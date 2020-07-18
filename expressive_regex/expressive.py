import re
import string
from typing import Union, Optional, List
from .aux_classes import Stack, StackFrame
from .regex_classes import *

specialChars = ['\\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-']

class ExpressiveRegex:
    __slosts__ = ('_expression', '_hasDefineStart', '_hasDefineEnd', '_flags', '_stack')
    def __init__(self):
        self._expression = ""
        self._hasDefineStart = False
        self._hasDefineEnd = False
        self._flags = {
            'i': False, # case-insensitive matching
            'm': False, # multiline
        }
        self._stack = Stack()
        self._stack.push(StackFrame(Root))

    @property
    def _currentFrame(self):
        return self._stack.top()

    def range(self, begin: Union[str,int], end: Union[str,int],
            exclude: Optional[Union[List[Union[str,int]], str]]=None):
        element = Range(begin, end, exclude)
        self._currentFrame.elements.append(element)

