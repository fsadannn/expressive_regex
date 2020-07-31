import copy

class Stack: # pragma: no cover
    __slots__ = tuple(['_stack'])

    def __init__(self):
        self._stack = []

    def copy(self):
        res = Stack()
        res._stack = copy.deepcopy(self._stack)
        return res

    def __len__(self):
        return len(self._stack)

    @property
    def empty(self):
        return len(self._stack) == 0

    def isempty(self):
        return len(self._stack) == 0

    def top(self):
        if len(self._stack) == 0:
            raise IndexError('pop from empty Stack')
        return self._stack[-1]

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if len(self._stack) == 0:
            raise IndexError('pop from empty Stack')
        val = self._stack.pop()
        return val


class StackFrame: # pragma: no cover
    __slots__ = ('_elements', '_quantifier', '_type',
                 '_quantifier_args', '_quantifier_kwargs')
    def __init__(self, cls):
        self._elements = []
        self._quantifier = None
        self._quantifier_args = ()
        self._quantifier_kwargs = {}
        self._type = cls

    def get_instance(self):
        return self._type(self._elements)

    def get_qinstance(self, instance=None):
        args = self._quantifier_args
        kwargs = self._quantifier_kwargs
        if instance:
            return self._quantifier(instance, *args, **kwargs)
        return self._quantifier(self.get_instance(), *args, **kwargs)

    def append(self, element):
        self._elements.append(element)

    @property
    def elements(self):
        return self._elements

    @property
    def quantifier(self):
        return self._quantifier

    @property
    def type(self):
        return self._type

    @quantifier.setter
    def quantifier(self, value):
        self._quantifier = value
