import re
import copy
from typing import Union, Optional, List
from .aux_classes import Stack, StackFrame
### Grouping
from .regex_classes import Capture
### Quatifiers
from .regex_classes import OptionalQ
from .regex_classes import zeroOrMore, zeroOrMoreLazy
from .regex_classes import oneOrMore, oneOrMoreLazy
### Others
from .regex_classes import Root
### Literals
from .regex_classes import anyChar, whitespaceChar
from .regex_classes import nonWhitespaceChar, Digit
from .regex_classes import nonDigit, Alphanum, nonAlphanum
from .regex_classes import Char, rawChar, String, rawString
from .regex_classes import Newline, carriageReturn, Tab, Space
from .regex_classes import Range, anythingButRange
from .regex_classes import anyOfChars, anythingButChars

class BadStatement(Exception):
    pass

class ExpressiveRegex:
    __slosts__ = ('_expression', '_hasDefineStart', '_hasDefineEnd', '_flags', '_stack')
    def __init__(self, mutable=True):
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
        self._mutable = mutable

    @property
    def mutable(self):
        return self._mutable

    @property
    def _currentFrame(self): # pragma: no cover
        return self._stack.top()

    def _applyQuatifier(self, element): # pragma: no cover
        if self._currentFrame.quantifier:
            wrap = self._currentFrame.get_qinstance(element)
            self._currentFrame.quantifier = None
        else:
            wrap = element
        return wrap

    def _matchElement(self, cls, *args, **kwargs): # pragma: no cover
        element = cls(*args, **kwargs)
        wrap = self._applyQuatifier(element)
        self._currentFrame.elements.append(wrap)
        return self

    def _instance(self): # pragma: no cover
        if self._mutable:
            return self
        obj = copy.deepcopy(self)
        obj._expression = ""
        return obj

    def _quantifier(self, qclass):
        if self._currentFrame.quantifier is not None:
            raise BadStatement(f'cannot quantify regular expression with "{str(qclass)}" because it\'s already being quantified with "{self._currentFrame.quantifier}"')
        instance = self._instance()
        instance._currentFrame.quantifier = qclass
        return instance

    ### Quantifiers

    @property
    def optional(self):
        return self._quantifier(OptionalQ)

    @property
    def zeroOrMore(self):
        return self._quantifier(zeroOrMore)

    @property
    def zeroOrMoreLazy(self):
        return self._quantifier(zeroOrMoreLazy)

    @property
    def oneOrMore(self):
        return self._quantifier(oneOrMore)

    @property
    def oneOrMoreLazy(self):
        return self._quantifier(oneOrMoreLazy)

    ### Grouping

    def end(self):
        if len(self._stack) == 1:
            raise BadStatement("Cannot call end while building the root expression.")
        instance = self._instance()
        frame = instance._stack.pop()
        wrap = instance._applyQuatifier(frame.get_instance())
        instance._currentFrame.append(wrap)
        return instance

    @property
    def capture(self):
        instance = self._instance()
        newFrame = StackFrame(Capture)
        instance._stack.push(newFrame)
        return instance

    ### Literals

    @property
    def anyChar(self):
        instance = self._instance()
        return instance._matchElement(anyChar)

    @property
    def whitespaceChar(self):
        instance = self._instance()
        return instance._matchElement(whitespaceChar)

    @property
    def nonWhitespaceChar(self):
        instance = self._instance()
        return instance._matchElement(nonWhitespaceChar)

    @property
    def digit(self):
        instance = self._instance()
        return instance._matchElement(Digit)

    @property
    def nonDigit(self):
        instance = self._instance()
        return instance._matchElement(nonDigit)

    @property
    def alphanum(self):
        instance = self._instance()
        return instance._matchElement(Alphanum)

    @property
    def nonAlphanum(self):
        instance = self._instance()
        return instance._matchElement(nonAlphanum)

    @property
    def newline(self):
        instance = self._instance()
        return instance._matchElement(Newline)

    @property
    def carriageReturn(self):
        instance = self._instance()
        return instance._matchElement(carriageReturn)

    @property
    def tab(self):
        instance = self._instance()
        return instance._matchElement(Tab)

    @property
    def space(self):
        instance = self._instance()
        return instance._matchElement(Space)


    def char(self, value):
        instance = self._instance()
        return instance._matchElement(Char, value)

    def rawChar(self, value):
        instance = self._instance()
        return instance._matchElement(rawChar, value)

    def string(self, value):
        instance = self._instance()
        return instance._matchElement(String, value)

    def rawString(self, value):
        instance = self._instance()
        return instance._matchElement(rawString, value)

    def range(self, begin: Union[str, int], end: Union[str, int],
              exclude: Optional[Union[List[Union[str, int]], str]]=None):
        instance = self._instance()
        return instance._matchElement(Range, begin, end, exclude)

    def anythingButRange(self, begin: Union[str, int], end: Union[str, int],
                         exclude: Optional[Union[List[Union[str, int]], str]]=None):
        instance = self._instance()
        return instance._matchElement(anythingButRange, begin, end, exclude)

    def anyOfChars(self, value):
        instance = self._instance()
        return instance._matchElement(anyOfChars, value)

    def anythingButChars(self, value):
        instance = self._instance()
        return instance._matchElement(anythingButChars, value)


    ### Build Expression

    def toRegexString(self)->String:
        txt = 'Cannot compute the value of a not yet fully specified regex object.\n'
        txt += f'(Try adding a .end() call to match the "{str(self._currentFrame._type)}")\n'
        assert len(self._stack) == 1, txt
        if not self._mutable and self._expression:
            return self._expression
        exp = self._currentFrame.get_instance().value
        self._expression = exp
        return exp

    def toRegex(self)->re.Pattern:
        exp = self.toRegexString()
        return re.compile(exp)
