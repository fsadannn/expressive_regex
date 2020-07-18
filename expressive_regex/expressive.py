import re
import string
from typing import Union, Optional, List
from .aux_classes import Stack, StackFrame
### Grouping
from .regex_classes import Capture
### Quatifiers
from .regex_classes import OptionalQ
### Others
from .regex_classes import Root
from .regex_classes import Range

specialChars = ['\\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-']

class BadStatement(Exception): pass

class ExpressiveRegex:
    # TODO: write as inmutable object, return a copy of the class instead the intance in each method
    __slosts__ = ('_expression', '_hasDefineStart', '_hasDefineEnd', '_flags', '_stack')
    def __init__(self, ):
        self._expression = ""
        self._hasDefineStart = False
        self._hasDefineEnd = False
        self._flags = {
            # TODO: add the other flags
            'i': False, # case-insensitive matching
            'm': False, # multiline
        }
        self._stack = Stack()
        self._stack.push(StackFrame(Root))

    @property
    def _currentFrame(self):
        return self._stack.top()

    def _applyQuatifier(self, element):
        if self._currentFrame.quantifier:
            wrap = self._currentFrame.get_qinstance(element)
            self._currentFrame.quantifier = None
        else:
            wrap = element
        return wrap

    ### Quantifiers

    @property
    def optional(self):
        self._currentFrame.quantifier = OptionalQ
        return self

    ### Grouping

    def end(self):
        if len(self._stack) == 1:
            raise BadStatement("Cannot call end while building the root expression.")
        frame = self._stack.pop()
        wrap = self._applyQuatifier(frame.get_instance())
        self._currentFrame.append(wrap)
        return self

    @property
    def capture(self):
        newFrame = StackFrame(Capture)
        self._stack.push(newFrame)
        return self

    ### Other

    def range(self, begin: Union[str,int], end: Union[str,int],
            exclude: Optional[Union[List[Union[str,int]], str]]=None):
        element = Range(begin, end, exclude)
        self._currentFrame.elements.append(element)

