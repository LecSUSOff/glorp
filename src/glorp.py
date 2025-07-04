from lark import Lark, Transformer
import sys
from typeguard import typechecked
import types
import linecache

VERSION = "1.0.3"

prefix = """
from typeguard import typechecked
class _GlorpWatcher:
    def __init__(self, initial_value, handler_func):
        self._val = initial_value
        self._handler = handler_func

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, new_val):
        old_val = self._val
        self._val = new_val
        if old_val != new_val:
            self._handler(new_val)

"""

grammar = open('grammar.lark', encoding='utf8').read()

parser = Lark(grammar)

class Glorp(Transformer):
    vartype: dict[str, str] = {}

    def __init__(self):
        super().__init__()
        self.stats = []
        self.watched_vars = set()

    def _indent(self, text_block, indent_str="    "):
        return "\n".join(indent_str + line for line in text_block.split('\n'))

    def _py_type(self, type_token):
        glorp_type = type_token.value
        match glorp_type:
            case "Int": return "int"
            case "Str": return "str"
            case "Null": return "None"
            case "Bool": return "bool"
            case "List": return "list"
            case "Dict": return "dict"
        print(f"Unknown type '{glorp_type}' on position {type_token.line}:{type_token.column}")
        exit()

    def name(self, n):
        var_name = '.'.join(n)
        if var_name in self.watched_vars:
            if len(n) == 1:
                return f"{var_name}.value"
        return var_name
          
    def watch_stmt(self, items):
            glorp_type, var_name, initial_value, handler_code = items
            
            self.watched_vars.add(var_name)

            if isinstance(handler_code, list):
                handler_code_block = "\n".join(handler_code)
            else:
                handler_code_block = handler_code

            handler_func_name = f"_glorp_handler_for_{var_name}"
            handler_func = f"def {handler_func_name}({var_name}):\n{self._indent(handler_code_block)}"

            watcher_instance = f"{var_name} = _GlorpWatcher({initial_value}, {handler_func_name})"

            return f"{handler_func}\n{watcher_instance}"

    def start(self, items):
        return "\n\n".join(items)

    def global_statement(self, items):
        return items[0]
          
    def import_stmt(self, items):
        module_name: str = items[0]
        module_transformer = Glorp()
        try:
            module_source = open(f'{module_name}.glorp', encoding='utf8').read()
            transformed_body = module_transformer.transform(parser.parse(module_source))
        except FileNotFoundError:
            raise Exception(f"Module '{module_name}' not found.")
        stats_to_delete = module_transformer.stats
        class_body = self._indent(transformed_body) if transformed_body else "    pass"
        del_statements = [f"del {var}" for var in stats_to_delete]
        cleanup_body = self._indent('\n'.join(del_statements))
        return f"class {module_name}:\n{class_body}\n\n{cleanup_body}" if cleanup_body else f"class {module_name}:\n{class_body}"
 
    def private(self, items):
        type_name, var_name, expression_str = items
        self.stats.append(var_name)
        py_type = self._py_type(type_name)
        return f"{var_name}: {py_type} = {expression_str}"
    
    def var_change(self, items):
        try: self.vartype[items[0]]
        except: 
            print(f'Variable not found {items[0]}')
            sys.exit(1)
        return f'{items[0]}: {self.vartype[items[0]]} = {items[1]}'

    def var_decl(self, items):
        if items[1] in self.vartype.keys():
            print(f'Variable {items[0]} is has been declared')
            sys.exit(1)
        self.vartype[items[1]] = self._py_type(items[0])
        if len(items) < 3:
            return f'{items[1]}: {self._py_type(items[0])} = None'
        type_name, var_name, expression_str = items
        if var_name in self.watched_vars:
            return f"{var_name}.value = {expression_str}"
        else:
            return f"{var_name}: {self._py_type(type_name)} = {expression_str}"
        
    def try_stmt(self, items):
        return f"try: \n{self._format_block(items[0])}\nexcept Exception as exception: \n{self._format_block(items[1])}"

    def func_short(self, items):
        return_type, func_name, *rest = items
        expression_str = rest[-1]
        params_str = rest[0] if len(rest) > 1 else ""
        py_return_type = self._py_type(return_type)
        return f"@typechecked\ndef {func_name}({params_str}) -> {py_return_type}:\n    return {expression_str}"

    def func_long(self, items):
        return_type, func_name, *rest = items
        body_statements = rest[-1]
        params_str = rest[0] if len(rest) > 1 else ""
        py_return_type = self._py_type(return_type)
        indented_body = "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"
        return f"@typechecked\ndef {func_name}({params_str}) -> {py_return_type}:\n{indented_body}"
    
    def body(self, items):
        return items
    
    def local_statement(self, items):
        return items[0]
        
    def out_stmnt(self, items):
        args_str = items[0] if items else ""
        return f'print({args_str})'
        
    def return_stmnt(self, items):
        return f'return {items[0]}'

    def if_stmnt(self, items):
        code = []
        count = len(items)
        has_else = count % 2 == 1
        limit = count - 1 if has_else else count
        for i in range(0, limit, 2):
            condition = items[i]
            body = items[i + 1]
            keyword = "if" if i == 0 else "elif"
            code.append(f"{keyword} {condition}:\n{self._format_block(body)}")
        if has_else:
            else_body = items[-1]
            code.append(f"else:\n{self._format_block(else_body)}")
        return "\n".join(code)

    def _format_block(self, body_statements):
        return "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"

    def while_stmnt(self, items):
        condition, body_statements = items
        indented_body = "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"
        return f"while {condition}:\n{indented_body}"
    
    def for_loop(self, items):
        _, var_name, start, end, body_statements = items
        step = 1
        indented_body = "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"
        return f"for {var_name} in range({start}, {end} + {step}, {step}):\n{indented_body}"

    def expression(self, items): return items[0]
    def logic_or(self, items): return f"({f' or '.join(items)})" if len(items) > 1 else items[0]
    def logic_and(self, items): return f"({f' and '.join(items)})" if len(items) > 1 else items[0]
    def logic_not(self, items):
        return items[0]
    
    def array_elements(self, items): return items
    def dictionary_elements(self, items): return items
    def dictionary_element(self, items):
        # items будет списком [key, value] из грамматики
        key, value = items
        # Возвращаем готовую строку "key: value"
        return f"{key}: {value}"

    def logic_unary_not(self, items):
        return f"(not ({items[0]}))"
    def comparison(self, items): return f"({items[0]} {items[1]} {items[2]})" if len(items) > 1 else items[0]
    def arith_exp(self, items): return " ".join(str(i) for i in items)
    def term(self, items): return " ".join(str(i) for i in items)
    def factor(self, items): return f"({items[0]})" if isinstance(items[0], str) and ' ' in items[0] else items[0]
    def call(self, items):
        func_name = items[0]
        args_str = items[-1] if len(items) > 1 else ""
        return f"{func_name}({args_str})"
    def arguments(self, items): return ", ".join(items)
    def parameters(self, items):
        params_list = []
        for i in range(0, len(items), 2):
            param_type_token = items[i]
            py_type = self._py_type(param_type_token)
            
            param_name = items[i+1] 
            
            params_list.append(f"{param_name}: {py_type}")
        return ", ".join(params_list)
    
    def array(self, items):
        if not items:
            return "[]"
        
        elements = items[0]
        
        return f"[{', '.join(map(str, elements))}]"
    
    def dictionary(self, items):
        if not items:
            return "{}"
        
        elements = items[0]
        
        return "{" + ', '.join(map(str, elements)) + "}"

    def element(self, items): return f'{items[0]}[{items[1]}]'
    
    def clear(self, _): return 'print("\033[H\033[2J")'

    def op_bool(self, items): return items[0]
    def op_exp(self, items): return items[0]
    def op_term(self, items): return items[0]
    def OP_ADD(self, token): return token.value
    def OP_SUB(self, token): return token.value
    def OP_MUL(self, token): return token.value
    def OP_DIV(self, token): return token.value
    def OP_POW(self, token): return "**" 
    def OP_EQ(self, token): return token.value
    def OP_NE(self, token): return token.value
    def OP_GT(self, token): return token.value
    def OP_LT(self, token): return token.value
    def OP_GE(self, token): return token.value
    def OP_LE(self, token): return token.value

    def TYPE(self, t): return t
    def NAME(self, n): return n.value
    def NUMBER(self, num): return int(num.value)
    def STRING(self, s): return s

if len(sys.argv) < 2:
    print("Usage: glorp <source_file.glorp> (you may use some additional flags)")
    sys.exit()

if sys.argv[1] in ['--ver', '-v', '--version']:
    print(VERSION)
    sys.exit()

try:
    source_code = open(sys.argv[1], encoding ='utf8').read()
    if source_code.strip() == '':
        print('Could not parse empty file!')
        sys.exit(1)
except FileNotFoundError:
    print(f"Error: File or argument '{sys.argv[1]}' not found.")
    sys.exit(1)


tree = parser.parse(source_code)

py_code = prefix + Glorp().transform(tree)

py_code += '''
Main()
'''

module_name = "glorp_runtime_module"
fake_filename = f"<{module_name}>"

glorp_module = types.ModuleType(module_name)

glorp_module.__file__ = fake_filename
glorp_module.typechecked = typechecked

lines = [line + '\n' for line in py_code.splitlines()]
linecache.cache[fake_filename] = (len(py_code), None, lines, fake_filename)

sys.modules[module_name] = glorp_module

try:
    exec(py_code, glorp_module.__dict__)
except Exception as e:
    print(f"An error occurred during execution: {e}", file=sys.stderr)
