
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


class Container_Meta(type):
    def __repr__(cls):
        return f"Container {cls.__name__}"

class Field_Meta(type):
    def __repr__(cls):
        container = cls.__module__
        if hasattr(cls, '__qualname__') and '.' in cls.__qualname__:
            container = cls.__qualname__.split('.')[0]
        return f"Fied {cls.__name__} of container {container}"

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
 #Expected line in your glorp file: 2 (This feature is experimental and might not work with multiline comments and empty lines)

 #Expected line in your glorp file: 4 (This feature is experimental and might not work with multiline comments and empty lines)


def Main():
    val = 1 / 0 #Expected line in your glorp file: 5 (This feature is experimental and might not work with multiline comments and empty lines) #Expected line in your glorp file: 7 (This feature is experimental and might not work with multiline comments and empty lines)

try:
    res = Main()
    if res: print("Programm finished with the result of", res)
except KeyboardInterrupt:
    print("Interrupted by user.")
    sys.exit(1)
