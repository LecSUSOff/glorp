from lark import Lark, Transformer
import sys
from typeguard import typechecked
import types
import linecache

VERSION = "1.0.4"

prefix = r"""
from typeguard import typechecked
import sys

# ==============================================================================
# Glorp System Classes
# ==============================================================================

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

# ==============================================================================
# Glorp Built-in Functions
# ==============================================================================

def out(*args):
    output_string = "".join(map(str, args))
    sys.stdout.write(output_string)
    sys.stdout.flush()

def clear():
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()

def readfile(filename: str) -> str:
    with open(filename, 'r', encoding='utf8') as f:
        return f.read()

def writefile(filename: str, content: str):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(content)

def read(prompt: str = "") -> str:
    return input(prompt)

def read_str(prompt: str = "") -> str:
    return input(prompt)

def read_int(prompt: str = "") -> int:
    while True:
        s = input(prompt)
        try:
            return int(s)
        except ValueError:
            out("Invalid input. Please enter a whole number (integer).\n")

def read_float(prompt: str = "") -> float:
    while True:
        s = input(prompt)
        try:
            return float(s)
        except ValueError:
            out("Invalid input. Please enter a number (e.g., 123 or 45.67).\n")

def read_bool(prompt: str = "") -> bool:
    while True:
        s = input(prompt).lower().strip()
        if s in ('true', 't', 'yes', 'y', '1'):
            return True
        elif s in ('false', 'f', 'no', 'n', '0'):
            return False
        else:
            out("Invalid input. Please enter 'true' or 'false'.\n")

true = True
false = False

"""

grammar = r'''
start: global_statement+

global_statement: import_stmt | var_decl | func_short | func_long | private | watch_stmt

local_statement: var_decl | return_stmnt |  if_stmnt | while_stmnt | for_loop | watch_stmt | var_change | call
 
import_stmt: "use" name

var_decl: "let" TYPE name "=" expression
var_change: "set" name "=" expression
private: "private" TYPE name "=" expression
func_short: "fn" TYPE name "(" parameters? ")" "=>" expression
watch_stmt: "watch" TYPE NAME "=" expression "->" (local_statement | ("{" body "}"))
return_stmnt: "=>" expression

func_long: "fn" TYPE name "(" parameters? ")" "{" body "}"

if_stmnt: "if" expression "{" body "}" ("elif" expression "{" body "}")* ("else" "{" body "}")?
while_stmnt: "while" expression "{" body "}"
for_loop: "for" "let" TYPE NAME "=" expression "to" expression "{" body "}"

body: local_statement*

TYPE: NAME

parameters: TYPE name ("," TYPE name)*
expression: logic_or

logic_or: logic_and ("or" logic_and)*
logic_and: logic_not ("and" logic_not)*
logic_not: "not" logic_not -> logic_unary_not
         | comparison
comparison: arith_exp (op_bool arith_exp)?

arith_exp: term (op_exp term)*
term: factor (op_term factor)*
factor: NUMBER
      | STRING
      | name
      | "(" expression ")"
      | call
      | array
      | dictionary
      | element

?op_exp: OP_ADD | OP_SUB
OP_ADD: "+"
OP_SUB: "-"

?op_term: OP_MUL | OP_DIV | OP_POW
OP_MUL: "*"
OP_DIV: "/"
OP_POW: "^"

?op_bool: OP_EQ | OP_NE | OP_GT | OP_LT | OP_GE | OP_LE
OP_EQ: "=="
OP_NE: "!="
OP_GT: ">"
OP_LT: "<"
OP_GE: ">="
OP_LE: "<="

call: name "(" [arguments] ")"

array: "[" [array_elements] "]"
dictionary: "{" dictionary_elements "}"
element: NAME "[" expression "]"

name: NAME("."NAME)*

arguments: expression ("," expression)*
array_elements: expression ("," expression)*
dictionary_element: expression ":" expression
dictionary_elements: dictionary_element ("," dictionary_element)*

%import common.CNAME
%import common.ESCAPED_STRING

%import common.CNAME -> NAME
%import common.SIGNED_NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING
%import common.WS

SINGLE_LINE_COMMENT: /\/\/[^\n]*/
MULTI_LINE_COMMENT_STD: /\/\*[\s\S]*?\*\//

%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT_STD
%import common.WS
%ignore WS'''

parser = Lark(grammar)

class Glorp(Transformer):
    def __init__(self):
        super().__init__()
        self.stats = []
        self.watched_vars = set()
        self.declared_functions = {
            "out", "clear",
            "read", "read_str", "read_int", "read_float", "read_bool",
            "readfile", "writefile"
        }
        self.vartype: dict[str, str] = {}

    def _indent(self, text_block, indent_str="    "):
        return "\n".join(indent_str + line for line in text_block.split('\n'))

    def _py_type(self, type_token):
        glorp_type = type_token.value
        match glorp_type:
            case "Int": return "int"
            case "Float": return "float"
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

            self.vartype[f'{var_name}.value'] = self._py_type(glorp_type)

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
        if func_name in self.declared_functions:
            print(f"Warning: Redefining function '{func_name}'")

        self.declared_functions.add(func_name)
        expression_str = rest[-1]
        params_str = rest[0] if len(rest) > 1 else ""
        py_return_type = self._py_type(return_type)
        return f"@typechecked\ndef {func_name}({params_str}) -> {py_return_type}:\n    return {expression_str}"

    def func_long(self, items):
        return_type, func_name, *rest = items
        if func_name in self.declared_functions:
            print(f"Warning: Redefining function '{func_name}'")

        self.declared_functions.add(func_name)
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
        key, value = items
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
        if '.' not in func_name and func_name not in self.declared_functions:
            # Здесь мы не можем получить номер строки, т.к. items - это уже обработанные строки.
            # Но мы можем выдать осмысленную ошибку.
            print(f"Error: Call to undefined function '{func_name}'.")
            sys.exit(1)

        args_str = items[-1] if len(items) > 1 else ""
        return f"{func_name}({args_str})"
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
    def NUMBER(self, num): return float(num.value) if '.' in num.value else int(num.value)
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

print(py_code)

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
