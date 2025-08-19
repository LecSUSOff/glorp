class Watcher:
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
def on_change(a, b):
    print(f'Значение было {b}, а стало {a}')
value = Watcher(5, on_change)
value.value = 6

