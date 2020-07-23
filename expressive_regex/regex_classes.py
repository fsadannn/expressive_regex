import abc
from typing import Union, Optional, List
import copy

specialChars = ['\\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-']

### Base
class Base(metaclass=abc.ABCMeta):
    __slosts__= ()
    @abc.abstractproperty
    def value(self):
        raise NotImplementedError

    def copy(self):
        return copy.deepcopy(self)

class BaseGroups(Base, metaclass=abc.ABCMeta):

    __slosts__ = ('_elements')
    def __init__(self, elements):
        self._elements = elements

    @classmethod
    def element(cls, elements):
        return cls(elements)


class BaseQuantifier(BaseGroups, metaclass=abc.ABCMeta):

    __slosts__ = ('_requiresGroup')
    def __init__(self, element, requiresGroup=False):
        assert not (isinstance(element, list) or isinstance(element, tuple))
        super().__init__(element)
        self._requiresGroup = requiresGroup

    @property
    def requiresGroup(self):
        return self._requiresGroup

    def _value(self):
        inner = self._elements.value
        grouping = f"(?:{inner})" if self._requiresGroup else inner
        return grouping

### Grouping
class Root(BaseGroups):
    __slosts__= ()
    @property
    def value(self):
        return "".join((i.value for i in self._elements))

class Capture(BaseGroups):
    __slosts__= ()
    @property
    def value(self):
        return "("+"".join((i.value for i in self._elements))+")"

### Quatifier
class OptionalQ(BaseQuantifier):
    __slosts__= ()
    @property
    def value(self):
        return self._value() + '?'


### Other

class Range(Base):
    __slosts__= ()
    def __init__(self, begin: Union[str,int], end: Union[str,int],
            exclude: Optional[Union[List[Union[str,int]], str]]=None):
        tb = type(begin)
        # TODO: write explanations of asserts
        assert (isinstance(begin, str) and len(begin)==1) or (isinstance(begin, int) and 0<=begin<=9)
        assert (isinstance(end, str) and len(end)==1) or (isinstance(end, int) and 0<=end<=9)
        assert begin<end
        if exclude:
            if isinstance(exclude, str):
                exclude=list(exclude)
            assert all([ ((isinstance(i, str) and len(i)==1) or (isinstance(i, int) and 0<=i<=9)) and type(i)==tb for i in exclude])
        self._begin = begin
        self._end = end
        self._exclude = exclude

    @property
    def value(self):
        pass

 ### Match Element
class anyChar(Base):
    __slosts__= ()

    @property
    def value(self):
        return '.'

class whitespaceChar(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\s'

class nonWhitespaceChar(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\S'

class Digit(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\d'

class nonDigit(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\D'

class Word(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\w'

class nonWord(Base):
    __slosts__= ()

    @property
    def value(self):
        return '\\W'