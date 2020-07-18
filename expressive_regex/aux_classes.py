

class Stack:
    __slots__ = ('_stack')
    def __init__(self):
        self._stack=[]

    def __len__(self):
        return len(self._stack)

    @property
    def empty(self):
        return len(self._stack)==0

    def isempty(self):
        return len(self._stack)==0

    def top(self):
        if len(self._stack)==0:
            raise IndexError('pop from empty Stack')
        return self._stack[-1]

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if len(self._stack)==0:
            raise IndexError('pop from empty Stack')
        val = self._stack.pop()
        return val


class StackFrame:
    __slots__ = ('_elements', '_quantifier', '_type')
    def __init__(self, cls):
        self._elements = []
        self._quantifier = None
        self._type = cls

    @property
    def elements(self):
        return self._elements

    @property
    def quantifier(self):
        return self._quantifier



