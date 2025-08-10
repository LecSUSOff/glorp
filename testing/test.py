'''
Testing new glorp features in python
'''

class PrettyMeta(type):
    def __repr__(cls):
        attrs = ", ".join(cls.__dict__.keys())
        return f"{cls.__name__}"

class MyClass(metaclass=PrettyMeta):
    x = 42

print(MyClass)
