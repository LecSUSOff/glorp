from lark import Lark, Transformer
import os
import sys
import types
import linecache
import time
import random
import string
import random
import os

import lark

start = time.time()

VERSION = "1.1.0"

py_prefix = r"""
from math import floor
from itertools import islice
import linecache
from types import SimpleNamespace
import sys
import subprocess
import os

def take(n, iterable):
    def generator():
        count = 0
        for item in iterable:
            if count >= n:
                break
            yield item
            count += 1
    return list(generator())

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
            self._handler(new_val, old_val)

def out(*args, sep=""):
    output_string = sep.join(map(str, args))
    sys.stdout.write(output_string)
    sys.stdout.flush()

def clear():
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()

def readfile(filename):
    with open(filename, 'r', encoding='utf8') as f:
        return f.read()

def writefile(filename, content):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(content)

def read(prompt=""):
    return input(prompt)

def read_str(prompt=""):
    return input(prompt)

def read_int(prompt=""):
    while True:
        s = input(prompt)
        try:
            return int(s)
        except ValueError:
            out("Invalid input. Please enter a whole number (integer).\n")

def read_float(prompt=""):
    while True:
        s = input(prompt)
        try:
            return float(s)
        except ValueError:
            out("Invalid input. Please enter a number (e.g., 123 or 45.67).\n")

def read_bool(prompt=""):
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

def pow(a, b):
    return a ** b

class NullType:
    def __repr__(self):
        return "Null"
    def __bool__(self):
        return False
    def __eq__(self, other):
        return other is None or isinstance(other, NullType)

class Object:
    def __init__(self, value):
        if isinstance(value, Object):
            self.__val__ = value.__val__
        else:
            self.__val__ = value

    def _unwrap(self, other):
        if isinstance(other, Object):
            return other.__val__
        return other

    def __eq__(self, other): return Object(self.__val__ == self._unwrap(other))
    def __ne__(self, other): return Object(self.__val__ != self._unwrap(other))
    def __lt__(self, other): return Object(self.__val__ < self._unwrap(other))
    def __le__(self, other): return Object(self.__val__ <= self._unwrap(other))
    def __gt__(self, other): return Object(self.__val__ > self._unwrap(other))
    def __ge__(self, other): return Object(self.__val__ >= self._unwrap(other))

    def __add__(self, other): return Object(self.__val__ + self._unwrap(other))
    def __sub__(self, other): return Object(self.__val__ - self._unwrap(other))
    def __mul__(self, other): return Object(self.__val__ * self._unwrap(other))
    def __truediv__(self, other): return Object(self.__val__ / self._unwrap(other))
    def __floordiv__(self, other): return Object(self.__val__ // self._unwrap(other)) # For Glorp's %%
    def __mod__(self, other): return Object(self.__val__ % self._unwrap(other))      # For Glorp's %
    def __pow__(self, other): return Object(self.__val__ ** self._unwrap(other))

    def __radd__(self, other): return Object(self._unwrap(other) + self.__val__)
    def __rsub__(self, other): return Object(self._unwrap(other) - self.__val__)
    def __rmul__(self, other): return Object(self._unwrap(other) * self.__val__)
    def __rtruediv__(self, other): return Object(self._unwrap(other) / self.__val__)
    def __rfloordiv__(self, other): return Object(self._unwrap(other) // self.__val__)
    def __rmod__(self, other): return Object(self._unwrap(other) % self.__val__)
    def __rpow__(self, other): return Object(self._unwrap(other) ** self.__val__)

    def __is__(self, other):
        other_val = self._unwrap(other)
        if isinstance(other_val, type):
            return isinstance(self.__val__, other_val)
        return self.__val__ == other_val
    
    def __iter__(self):
        for item in self.__val__:
            yield Object(item)

    def __getitem__(self, key):
        return Object(self.__val__[key])

    def __getattr__(self, name):
        return Object(getattr(self.__val__, name))

    def __str__(self): return str(self.__val__)
    __repr__ = __str__

def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")

def int_div(a, b):
    try:
        return a % b
    except ZeroDivisionError:
        return float("inf")

true = True
false = False
Null = NullType()
null = NullType()
num = eval

__glorp_last__ = Null
__vals__ = []
"""

def get_grammar_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, "grammar.lark")

with open(get_grammar_path(), "r", encoding="utf8") as f:
    grammar = f.read()

parser = Lark(grammar)
mainargs = False

immutes = {}

class Glorp(Transformer):
    def __init__(self, module_context_name=None):
        super().__init__()
        self.watched_vars = set()
        self.declared_symbols = {
            "out", "clear",
            "read", "read_str", "read_int", "read_float", "read_bool",
            "readfile", "writefile", "str", "int", "this"
        }
        self.private_vars = {}
        self.module_context_name = module_context_name
        self.ops = {
            "^" : "pow"
        }

    def _generate_mangled_name(self, original_name, context):
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"_{self.module_context_name}_{context}_{original_name}_{suffix}"
    
    def _generate_type_prefix(self, arg_string: str) -> str:
        arg_string = arg_string.strip()
        if not arg_string:
            return (
                "def __init__(self):\n"
                "    pass\n\n"
                "def __eq__(self, other):\n"
                "    return isinstance(other, type(self))\n\n"
                "def __is__(self, label):\n"
                "   return label in self.state or self.type == label\n\n"
            )

        parts = [part.strip() for part in arg_string.split(",") if part.strip()]

        init_args = []
        assignments = []
        arg_names = []

        for part in parts:
            if "=" in part:
                var, default = part.split("=", 1)
                var = var.strip()
                default = default.strip()
                init_args.append(f"{var}={default}")
            else:
                var = part
                init_args.append(var)
            assignments.append(f"self.{var} = {var}")
            arg_names.append(var)

        header = f"def __init__(self, {', '.join(init_args)}):"
        body = "\n".join(f"    {line}" for line in assignments)
        init_block = f"{header}\n{body}"

        eq_conditions = " and ".join([f"self.{var} == other.{var}" for var in arg_names])
        eq_block = (
            "def __eq__(self, other):\n"
            "    if not isinstance(other, type(self)): return False\n"
            f"    return {eq_conditions}"
        )
        is_block = (
            "def __is__(self, other):\n"
            "   if self == other: return True\n"
            "   if isinstance(other, type):\n"
            "       return isinstance(self, other)\n"
            "   return any(value == other for value in self.__dict__.values())\n"
        )
        repr_str = (
            "def __str__(self):\n"
            "   args = ', '.join(map(str, self.__dict__.values()))\n"
            "   return f\"{self.__class__.__name__}({args})\"\n"
            "__repr__ = __str__"
        )
        this_property = (
            "@property\n"
            "def this(self):\n"
            "    return self\n"
        )

        return f"{init_block}\n\n{eq_block}\n\n{is_block}\n\n{repr_str}\n\n{this_property}"


    def name(self, n):
        if n == []: return '__glorp_last__'
        def get_value(item):
            if hasattr(item, 'value'):
                return item.value
            return str(item)

        first_part_name = get_value(n[0])
        
        mangled_first_part = None

        if first_part_name in self.private_vars or first_part_name in immutes:
            if first_part_name in self.private_vars: mangled_name = self.private_vars[first_part_name]
            else: mangled_name = immutes[first_part_name]
            
            if self.module_context_name:
                mangled_first_part = f"{mangled_name}"
            else:
                mangled_first_part = mangled_name
        else:
            mangled_first_part = first_part_name
            
        rest_parts = [get_value(part) for part in n[1:]]
        full_name = ".".join([mangled_first_part] + rest_parts)
        
        return full_name

    def private(self, items):
        var_name, expression_str = items
        if var_name in self.private_vars:
            print(f"Warning: Private variable '{var_name}' is being redefined.")
        mangled_name = self._generate_mangled_name(var_name, "private")
        self.private_vars[var_name] = mangled_name
        return f"{mangled_name} = {expression_str}"
    
    def immute(self, items):
        var_name, expression_str = items
        if var_name in self.private_vars:
            print(f"Warning: Private variable '{var_name}' is being redefined.")
        mangled_name = self._generate_mangled_name(var_name, "constant")
        immutes[var_name] = mangled_name
        return f"{mangled_name} = {expression_str}"
    
    def lambda_call(self, items):
        expr_str = items[0]
        arg_str = items[1]
        
        arg_count = len(arg_str.split(','))
        arg_names = [chr(97 + i) for i in range(arg_count)]

        fn_code = f"(lambda {', '.join(arg_names)}: {expr_str})({arg_str})"

        return fn_code

    def import_stmt(self, items):
        path = items[-1].split('.')
        module_path = "/".join(path)
        module_name = path[-1] if len(items) == 1 else items[0]
        self.declared_symbols.add(module_name)
        
        module_fake_filename = f"<glorp_{module_path}_module>"

        try:
            with open(f"{module_path}.glorp", "r", encoding="utf8") as f:
                module_source = f.read()
        except FileNotFoundError:
            raise GlorpError(f"Module '{'/'.join(items)}' not found.")
        
        module_transformer = Glorp(module_context_name=module_name)
        tree = parser.parse(module_source)
        module_py_code = module_transformer.transform(tree)

        escaped_module_code = repr(module_py_code)

        return f"""
{module_name} = SimpleNamespace()
_glorp_module_code = {escaped_module_code}

_glorp_exec_dict = globals().copy()
_glorp_initial_keys = set(_glorp_exec_dict.keys())

_glorp_module_lines = [line + '\\n' for line in _glorp_module_code.splitlines()]
linecache.cache['{module_fake_filename}'] = (len(_glorp_module_code), None, _glorp_module_lines, '{module_fake_filename}')

exec(compile(_glorp_module_code, '{module_fake_filename}', 'exec'), _glorp_exec_dict)

for key, value in _glorp_exec_dict.items():
    if key not in _glorp_initial_keys:
        setattr({module_name}, key, value)

del _glorp_module_code, _glorp_exec_dict, _glorp_initial_keys, _glorp_module_lines
"""
    
    def py_import(self, items):
        self.declared_symbols.add(items[0])
        if len(items) == 1:
            return f'import {items[0]}'
        return f'import {items[1]} as {items[0]}'

    def named_arg(self, items):
        return f'{items[0]} = {items[1]}'
    
    def default_param(self, items):
        return f'{items[0]} = {items[1]}'
    
    def _indent(self, text_block, indent_str="    "):
        return "\n".join(indent_str + line for line in text_block.split('\n'))

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
        
    def list_comprehension(self, items):
        generator_expression = items[0]
        return f'list({generator_expression})'
    
    def int_div(self, items):
        return f'int_div({items[0]}, {items[1]})'

    def watch_stmt(self, items):
        var_name, initial_value, handler_code = items
        self.watched_vars.add(var_name)

        handler_code_block = "\n".join(handler_code) if isinstance(handler_code, list) else handler_code
        handler_func_name = f"_glorp_handler_for_{var_name}"

        handler_func = f"def {handler_func_name}(old, new):\n{self._indent(handler_code_block)}"
        watcher_instance = f"{var_name} = _GlorpWatcher({initial_value}, {handler_func_name})"
        return f"{handler_func}\n{watcher_instance}"

    def start(self, items):
        return "\n\n".join(items)

    def global_statement(self, items):
        return items[0]

    def var_decl(self, items):
        if items[0] in immutes.values(): raise GlorpSemanticError("Trying to change immutable " + items[0].split('_')[-2])
        self.declared_symbols.add(items[0])
        return f'{items[0]} = {items[1]}'
    
    def try_stmt(self, items):
        return f"try:\n{self._format_block(items[0])}\nexcept Exception as exception:\n{self._format_block(items[1])}"

    def throw(self, items):
        return f'raise Exception({items[0]})'

    def yield_stmt(self, items):
        return f'yield {items[0]}'

    def func(self, items):
        func_name, *rest = items
        if func_name in self.declared_symbols:
            print(f"Warning: Redefining function '{func_name}'")
        self.declared_symbols.add(func_name)
        
        params_str = (rest[0]) if len(rest) > 1 else ""
        body_statements = rest[-1] + ["return null"]
        indented_body = "\n".join(self._indent(s) for s in body_statements) if body_statements else "    pass"
        global mainargs

        if func_name == "Main" and params_str != "": mainargs = True
        
        return f"\ndef {func_name}({params_str}):\n{indented_body}"
    
    def class_def(self, items):
        if len(items) == 3:
            if ',' in items[1]:
                name, args, body_lines = items
                parent = ''
            else:
                name, parent, body_lines = items
                args = ''
        elif len(items) == 4:
            name, parent, args, body_lines = items
        else:
            name, body_lines = items
            args = parent = ''

        self.declared_symbols.add(name)

        return f'class {name}({parent}):\n{self._format_block(self._generate_type_prefix(args).split('\n'))}\n{self._format_block(body_lines)}'
    
    def container_def(self, items):
        name, *params = items
        res = (f'class {name}:\n'
        f'    def __str__(self):\n        return \'Container "{name}"\'')
        for param in params:
            res += f'\n    {param} = \'Field {param} of container {name}\''
        return res
    
    def prop_stmt(self, items):
        return f'@property\ndef {items[0]}(this):\n{self._format_block(items[1])}'

    def body(self, items):
        return items

    def local_statement(self, items):
        return items[0]

    def return_stmnt(self, items):
        return f'return {items[0]}'
    
    def switch_case(self, items: list[str]):
        exp = items[0]
        items = items[1:]
        code = [f"_val = {exp}", f"match _val:"]
        count = len(items)
        has_default = count % 2 == 1
        limit = count - 1 if has_default else count

        for i in range(0, limit, 2):
            condition, body = items[i], items[i+1]
            if 'grange' in condition or '[' in condition:
                code.append(
                    f"    case _ if _val in {condition} or _val == {condition}:\n   {self._format_block(body)}"
                )
            else:
                code.append(
                    f"    case _ if _val == {condition}:\n   {self._format_block(body)}"
                )

        if has_default:
            code.append(f"    case _:\n {self._format_block(items[-1])}")
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
        self.declared_symbols.add(var_name)
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
            return f'(({statement} if {if_block} else {else_block}) for {var_name} in {object_name})'

    def parameters(self, items):
        return ", ".join(map(str, items))

    def call(self, items):
        func_name: str = items[0]
        args_str = items[1] if len(items) > 1 else ""
        return f"{func_name}({args_str})"
    
    def neg(self, n): return f"-{n[0]}"
    def pos(self, n): return str(n[0])


    def safe_div(self, items): return f"safe_div({items[0]}, {items[1]})"
    def globalise(self, items): return f'global {items[0]}'
    def symbol(self, items): return items[0]
    def expression(self, items: list[str]):  return f'{items[0]}'
    def logic_is(self, items): return f'Object({items[0]}).__is__({items[1]})'
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

    error_type = type(e).__name__
    error_msg = str(e)

    if last_glorp_frame:
        line_num: int | None = last_glorp_frame.lineno
        code_line: str = linecache.getline(fake_filename, line_num if line_num else 0).strip()

        friendly_message = (
            f"Runtime Error in '{source_file}'\n\n"
            f"  Error Type: {error_type}\n"
            f"  Details: {error_msg}\n\n"
            f"The error occurred while executing the logic from your script.\n"
            f"The problematic operation in the generated Python code was:\n"
            f"  [{line_num}] > {code_line}\n\n"
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
        print("Usage: glorp [run | to-py] <source_file.glorp> (you may use some additional flags)")
        return

    if sys.argv[1] in ['--ver', '-v', '--version']:
        print(VERSION)
        return
        
    source_file = sys.argv[2]

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
            context = e.get_context(source_code, 40) if hasattr(e, 'get_context') else '' # type: ignore
            error_details = str(e)
            message = f"Invalid syntax.\n> {context}\nDetails: {error_details}"
            raise GlorpParseError(message, line=getattr(e, 'line', None), column=getattr(e, 'column', None))
            
        transformer = Glorp("Runtime")
        py_code = py_prefix + transformer.transform(tree)
        
        py_code += f'''

try:
    res = {"Main(sys.argv)" if mainargs else "Main()"}
    if res: print("Programm finished with the result of", res)
except KeyboardInterrupt:
    print("Interrupted by user.")
    sys.exit(1)
'''

        print(f'Took {time.time() - start} seconds to transpile\n' if '-o' in sys.argv else '', end='')

        start2 = time.time()

        module_name = "glorp_runtime_module"
        fake_filename = f"<{source_file}>"

        glorp_module = types.ModuleType(module_name)
        glorp_module.__file__ = fake_filename

        lines = [line + '\n' for line in py_code.splitlines()]
        linecache.cache[fake_filename] = (len(py_code), None, lines, fake_filename)
        sys.modules[module_name] = glorp_module
        
        try:
            print(py_code if '-d' in sys.argv else '', end = '')
            print(tree.pretty(' ') if '-t' in sys.argv else '', end = '')
            match sys.argv[1]:
                case 'to-py':
                    with open(source_file.rstrip('.glorp') + '.py', 'w') as f:
                        f.write(py_code)
                case 'run':
                    compiled_code = compile(py_code, fake_filename, 'exec')
                    exec(compiled_code, glorp_module.__dict__)
            
        except Exception as e:
            handle_runtime_error(e, fake_filename, source_file)
        
        print(f'\nTook {time.time() - start2} seconds to execute' if '-o' in sys.argv else '', end='')
        print(f'\nTook {time.time() - start} seconds in total' if '-o' in sys.argv else '', end='')

    except GlorpError as e:
        print(f"--- Glorp Error ---", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        sys.exit(1)

    except lark.exceptions.VisitError as e:
        print(f"--- Glorp Syntax Error ---", file=sys.stderr)
        print(f"{e.orig_exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
