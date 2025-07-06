from lark import Lark, Transformer
import sys
import types
import linecache
from itertools import islice

class GlorpError(Exception):
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        if self.line and self.column:
            return f"[Line {self.line}:{self.column}] {self.message}"
        elif self.line:
            return f"[Line {self.line}] {self.message}"
        return self.message

class GlorpParseError(GlorpError):
    pass

class GlorpSemanticError(GlorpError):
    pass

class GlorpRuntimeError(GlorpError):
    pass

VERSION = "1.0.6"

prefix = r"""
from typeguard import typechecked
from itertools import islice
import sys
from typing import *

T = TypeVar('T')

def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    def generator():
        count = 0
        for item in iterable:
            if count >= n:
                break
            yield item
            count += 1
    return generator()

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

def grange(start, end, step=None):
    if step is None:
        step = 1 if end >= start else -1

    if step == 0:
        raise ValueError("grange() step argument must not be zero")

    # Используем 1e-9 для безопасного сравнения float
    current = float(start)
    end = float(end)
    
    if step > 0:
        while current <= end + 1e-9:
            yield round(current, 10)
            current += step
    else: # step < 0
        while current >= end - 1e-9:
            yield round(current, 10)
            current += step

true = True
false = False

"""

grammar = open('grammar.lark', encoding='utf8').read()

parser = Lark(grammar)

class Glorp(Transformer):
    def __init__(self):
        super().__init__()
        self.stats = []
        self.watched_vars = set()
        self.scopes: list[dict[str, str]] = [{}]
        self.declared_functions = {
            "out", "clear",
            "read", "read_str", "read_int", "read_float", "read_bool",
            "readfile", "writefile", "str", "int"
        }

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare_variable(self, name: str, py_type: str, line=None, column=None):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise GlorpSemanticError(f"Variable '{name}' is already declared in this scope.", line, column)
        current_scope[name] = py_type

    def find_variable_type(self, name: str) -> str | None:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def _indent(self, text_block, indent_str="    "):
        return "\n".join(indent_str + line for line in text_block.split('\n'))

    def _py_type(self, type_token):
        glorp_type = type_token
        match glorp_type:
            case "Int": return "int"
            case "Float": return "float"
            case "Str": return "str"
            case "Null": return "None"
            case "Bool": return "bool"
            case "List": return "list"
            case "Dict": return "dict"
        raise GlorpSemanticError(
            f"Unknown type '{glorp_type}'",
            line=type_token.line,
            column=type_token.column
        )

    def name(self, n):
        var_name = '.'.join(i.value for i in n)
        return var_name

    def num_range(self, items):
        if len(items) == 2:
            start_expr = str(items[0])
            end_expr = str(items[1])
            return f"grange({start_expr}, {end_expr})"
        elif len(items) == 3:
            start_expr = str(items[0])
            mid_expr = str(items[1])
            end_expr = str(items[2])
            return f"grange({start_expr}, {end_expr}, {mid_expr} - {start_expr})"

    def watch_stmt(self, items):
        glorp_type, var_name_token, initial_value, handler_code = items
        var_name = var_name_token
        
        self.watched_vars.add(var_name)
        py_type = self._py_type(glorp_type)
        self.declare_variable(var_name, py_type)

        handler_code_block = "\n".join(handler_code) if isinstance(handler_code, list) else handler_code
        handler_func_name = f"_glorp_handler_for_{var_name}"

        self.enter_scope()
        self.declare_variable(var_name, py_type)
        handler_func = f"def {handler_func_name}({var_name}):\n{self._indent(handler_code_block)}"
        self.exit_scope()

        watcher_instance = f"{var_name} = _GlorpWatcher({initial_value}, {handler_func_name})"
        return f"{handler_func}\n{watcher_instance}"

    def start(self, items):
        return "\n\n".join(items)

    def global_statement(self, items):
        return items[0]

    def import_stmt(self, items):
        module_name = items[0]
        module_transformer = Glorp()
        try:
            with open(f'{module_name}.glorp', 'r', encoding='utf8') as f:
                module_source = f.read()
            tree = parser.parse(module_source)
            transformed_body = module_transformer.transform(tree)
        except FileNotFoundError:
            raise GlorpError(f"Module '{module_name}' not found.")
        
        stats_to_delete = module_transformer.stats
        class_body = self._indent(transformed_body) if transformed_body else "    pass"
        del_statements = [f"del {var}" for var in stats_to_delete]
        cleanup_body = self._indent('\n'.join(del_statements))
        return f"class {module_name}:\n{class_body}\n\n{cleanup_body}" if cleanup_body else f"class {module_name}:\n{class_body}"

    def private(self, items):
        type_token, var_name_token, expression_str = items
        var_name = var_name_token
        self.stats.append(var_name)
        py_type = self._py_type(type_token)
        self.declare_variable(var_name, py_type)
        return f"{var_name}: {py_type} = {expression_str}"

    def var_change(self, items):
        var_name, expression = items[0], items[1]
        var_py_type = self.find_variable_type(var_name)
        if var_py_type is None:
            raise GlorpSemanticError(f"Variable not found {var_name}")
        
        return f'{var_name}: {var_py_type} = {var_py_type}({expression})'

    def var_decl(self, items):
        type_token, var_name_token = items[0], items[1]
        var_name = var_name_token
        py_type = self._py_type(type_token)
        
        self.declare_variable(var_name, py_type)
        
        if len(items) < 3:
            return f'{var_name}: {py_type} = None'
        
        expression_str = items[2]
        if var_name in self.watched_vars:
            return f"{var_name}.value = {expression_str}"
        else:
            return f"{var_name}: {py_type} = {py_type}({expression_str})"

    def try_stmt(self, items):
        return f"try:\n{self._format_block(items[0])}\nexcept Exception as exception:\n{self._format_block(items[1])}"

    def throw(self, items):
        return f'raise Exception({items[0]})'

    def yield_stmt(self, items):
        return f'yield {items[0]}'

    def func_short(self, items):
        return_type, func_name_token, *rest = items
        func_name = func_name_token
        if func_name in self.declared_functions:
            print(f"Warning: Redefining function '{func_name}'")
        self.declared_functions.add(func_name)

        self.enter_scope()
        params_str = self.parameters(rest[0]) if len(rest) > 1 else ""
        expression_str = rest[-1]
        py_return_type = self._py_type(return_type)
        self.exit_scope()
        
        return f"@typechecked\ndef {func_name}({params_str}) -> {py_return_type}:\n    return {expression_str}"

    def func_long(self, items):
        return_type, func_name_token, *rest = items
        func_name = func_name_token
        if func_name in self.declared_functions:
            print(f"Warning: Redefining function '{func_name}'")
        self.declared_functions.add(func_name)
        
        self.enter_scope()
        params_str = self.parameters(rest[0]) if len(rest) > 1 else ""
        body_statements = rest[-1]
        py_return_type = self._py_type(return_type)
        indented_body = "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"
        self.exit_scope()
        
        return f"@typechecked\ndef {func_name}({params_str}) -> {py_return_type}:\n{indented_body}"

    def body(self, items):
        return items

    def local_statement(self, items):
        return items[0]

    def return_stmnt(self, items):
        return f'return {items[0]}'
    
    def switch_case(self, items):
        exp = items[0]
        items = items[1:]
        code = [f'match {exp}:']
        count = len(items)
        has_default = count % 2 == 1
        limit = count - 1 if has_default else count
        for i in range(0, limit, 2):
            condition, body = items[i], items[i+1]
            code.append(f"  case {condition}:\n{self._format_block(body.split('\n'))}")
        if has_default:
            code.append(f"  case _:\n{self._format_block(items[-1].split('\n'))}")
        return "\n".join(code)

    def if_stmnt(self, items):
        code = []
        count = len(items)
        has_else = count % 2 == 1
        limit = count - 1 if has_else else count
        for i in range(0, limit, 2):
            condition, body = items[i], items[i+1]
            keyword = "if" if i == 0 else "elif"
            code.append(f"{keyword} {condition}:\n{self._format_block(body)}")
        if has_else:
            code.append(f"else:\n{self._format_block(items[-1])}")
        return "\n".join(code)

    def _format_block(self, body_statements):
        return "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"

    def while_stmnt(self, items):
        condition, body_statements = items
        return f"while {condition}:\n{self._format_block(body_statements)}"

    def for_loop(self, items):
        var_name_token, start, end, body_statements = items
        var_name = var_name_token
        return f"for {var_name} in grange({start}, {end}):\n{self._format_block(body_statements)}"

    def for_each(self, items):
        var_name, object_name, body_statements = items
        return f'for {var_name} in {object_name}:\n{self._format_block(body_statements)}'

    def quick_foreach(self, items):
        if len(items) == 3:
            var_name, object_name, statement = items
            return f'({statement} for {var_name} in {object_name})'
        elif len(items) == 4:
            var_name, object_name, if_block, statement = items
            return f'({statement} for {var_name} in {object_name} if {if_block})'
        else:
            var_name, object_name, if_block, statement, else_block = items
            return f'({statement} if {if_block} else {else_block} for {var_name} in {object_name})'

    def parameters(self, items):
        params_list = []
        for i in range(0, len(items), 2):
            param_type_token, param_name_token = items[i], items[i+1]
            py_type = self._py_type(param_type_token)
            param_name = param_name_token
            self.declare_variable(param_name, py_type)
            params_list.append(f"{param_name}: {py_type}")
        return ", ".join(params_list)

    def call(self, items):
        func_name = items[0]
        if '.' not in func_name and func_name not in self.declared_functions:
            raise GlorpSemanticError(f"Call to undefined function '{func_name}'.")
        args_str = items[1] if len(items) > 1 else ""
        return f"{func_name}({args_str})"

    def expression(self, items): return items[0]
    def logic_or(self, items): return f"({f' or '.join(items)})" if len(items) > 1 else items[0]
    def logic_and(self, items): return f"({f' and '.join(items)})" if len(items) > 1 else items[0]
    def logic_not(self, items): return items[0]
    def logic_unary_not(self, items): return f"(not ({items[0]}))"
    def comparison(self, items): return f"({items[0]} {items[1]} {items[2]})" if len(items) > 1 else items[0]
    def arith_exp(self, items): return " ".join(str(i) for i in items)
    def term(self, items): return " ".join(str(i) for i in items)
    def factor(self, items): return f"({items[0]})" if isinstance(items[0], str) and ' ' in items[0] else items[0]
    def arguments(self, items): return ", ".join(map(str, items))
    def array(self, items): return f"[{', '.join(map(str, items[0]))}]" if items else "[]"
    def take_stmt(self, items): return f'take({items[0]}, {items[1]})'
    def dictionary(self, items): return "{" + ', '.join(map(str, items[0])) + "}" if items else "{}"
    def array_elements(self, items): return items
    def dictionary_elements(self, items): return items
    def dictionary_element(self, items): return f"{items[0]}: {items[1]}"
    def element(self, items): return f'{items[0]}[{items[1]}]'
    def op_bool(self, items): return items[0]
    def op_exp(self, items): return items[0]
    def op_term(self, items): return items[0]
    def OP_ADD(self, token): return token.value
    def OP_SUB(self, token): return token.value
    def OP_MUL(self, token): return token.value
    def OP_DIV(self, token): return '//' if token.value == r'%%' else token.value
    def OP_POW(self, token): return "**"
    def OP_EQ(self, token): return token.value
    def OP_NE(self, token): return token.value
    def OP_GT(self, token): return token.value
    def OP_LT(self, token): return token.value
    def OP_GE(self, token): return token.value
    def OP_LE(self, token): return token.value
    def TYPE(self, t): return t
    def NAME(self, n): return n
    def INF(self, _): return 'float("inf")'
    def pos_inf(self, _): return 'float("inf")'
    def neg_inf(self, _): return 'float("-inf")'
    def NUMBER(self, num): return float(num.value) if '.' in num.value else int(num.value)
    def STRING(self, s): return s.value

class GlorpError(Exception):
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        if self.line and self.column:
            return f"[Line {self.line}:{self.column}] {self.message}"
        elif self.line:
            return f"[Line {self.line}] {self.message}"
        return self.message

class GlorpParseError(GlorpError):
    pass

class GlorpSemanticError(GlorpError):
    pass

class GlorpRuntimeError(GlorpError):
    pass



def handle_runtime_error(e: Exception, fake_filename: str, source_file: str):
    import traceback
    tb = e.__traceback__
    
    last_glorp_frame = None
    for frame in traceback.extract_tb(tb):
        if frame.filename == fake_filename:
            last_glorp_frame = frame
            break

    error_type = type(e).__name__
    error_msg = str(e)

    if last_glorp_frame:
        line_num = last_glorp_frame.lineno
        code_line = linecache.getline(fake_filename, line_num).strip()

        friendly_message = (
            f"Runtime Error in '{source_file}'\n\n"
            f"  Error Type: {error_type}\n"
            f"  Details: {error_msg}\n\n"
            f"This error occurred while executing the logic that corresponds to line {line_num} "
            f"of the generated Python code.\n"
            f"The problematic operation in Python was:\n"
            f"  > {code_line}\n\n"
            f"Common causes for this error include division by zero, accessing a list element that doesn't exist, or type mismatches during an operation."
        )
        raise GlorpRuntimeError(friendly_message) from None
    else:
        friendly_message = (
            f"Runtime Error in '{source_file}'\n\n"
            f"  Error Type: {error_type}\n"
            f"  Details: {error_msg}\n\n"
            f"An error occurred during execution, but the exact location in your Glorp code could not be determined. "
            f"Please review your code for potential issues like invalid mathematical operations or incorrect function arguments."
        )
        raise GlorpRuntimeError(friendly_message) from None


def main():
    if len(sys.argv) < 2:
        print("Usage: glorp <source_file.glorp> (you may use some additional flags)")
        return

    if sys.argv[1] in ['--ver', '-v', '--version']:
        print(VERSION)
        return
        
    source_file = sys.argv[1]

    try:
        try:
            source_code = open(source_file, encoding='utf8').read()
            if not source_code.strip():
                return
        except FileNotFoundError:
            raise GlorpError(f"File '{source_file}' not found.")

        try:
            tree = parser.parse(source_code)
        except Exception as e:
            context = e.get_context(source_code, 40) if hasattr(e, 'get_context') else ''
            error_details = str(e)
            message = f"Invalid syntax.\n> {context}\nDetails: {error_details}"
            raise GlorpParseError(message, line=getattr(e, 'line', None), column=getattr(e, 'column', None))
            
        transformer = Glorp()
        py_code = prefix + transformer.transform(tree)
        
        py_code += '\n\nMain()\n'

        print(py_code)

        module_name = "glorp_runtime_module"
        fake_filename = f"<{source_file}>"

        glorp_module = types.ModuleType(module_name)
        glorp_module.__file__ = fake_filename

        lines = [line + '\n' for line in py_code.splitlines()]
        linecache.cache[fake_filename] = (len(py_code), None, lines, fake_filename)
        sys.modules[module_name] = glorp_module
        
        try:
            exec(py_code, glorp_module.__dict__)
        except Exception as e:
            handle_runtime_error(e, fake_filename, source_file)

    except GlorpError as e:
        print(f"--- Glorp Error ---", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"--- An Unexpected Internal Error Occurred ---", file=sys.stderr)
        print(e)

if __name__ == "__main__":
    main()