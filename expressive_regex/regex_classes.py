import abc
from typing import Union, Optional, List
import copy

specialChars = ['\\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-']
specialCharsd = {i:'\\'+i for i in specialChars}

def scape_special(values):
    nvalues = ""
    for i in values:
        if i in specialCharsd:
            nvalues += specialCharsd[i]
        else:
            nvalues += i
    return nvalues

### Base
class Base(metaclass=abc.ABCMeta): # pragma: no cover
    __slosts__ = ('_requiresGroup')
    def __init__(self, requiresGroup=False):
        self._requiresGroup = requiresGroup

    @property
    def requiresGroup(self):
        return self._requiresGroup

    @abc.abstractproperty
    def value(self):
        raise NotImplementedError

    def copy(self):
        return copy.deepcopy(self)

class BaseGroups(Base, metaclass=abc.ABCMeta): # pragma: no cover
    __slosts__ = ('_elements')
    def __init__(self, elements):
        super().__init__()
        self._elements = elements

    @classmethod
    def element(cls, elements):
        return cls(elements)


class BaseQuantifier(BaseGroups, metaclass=abc.ABCMeta): # pragma: no cover
    __slosts__ = ()
    def __init__(self, element):
        assert not isinstance(element, (list, tuple))
        super().__init__(element)

    def _value(self):
        inner = self._elements.value
        verif = not(len(inner)==1 or (len(inner)==2 and '\\' in inner))
        print(verif)
        grouping = f"(?:{inner})" if self._elements.requiresGroup and verif else inner
        return grouping

### Grouping
class Root(BaseGroups):
    __slosts__ = ()
    @property
    def value(self):
        return "".join((i.value for i in self._elements))

class Capture(BaseGroups):
    __slosts__ = ()
    @property
    def value(self):
        return "("+"".join((i.value for i in self._elements))+")"

### Quatifier
class OptionalQ(BaseQuantifier):
    __slosts__ = ()
    @property
    def value(self):
        return self._value() + '?'

class zeroOrMore(BaseQuantifier):
    __slosts__ = ()
    @property
    def value(self):
        return self._value() + '*'

class zeroOrMoreLazy(BaseQuantifier):
    __slosts__ = ()
    @property
    def value(self):
        return self._value() + '*?'

class oneOrMore(BaseQuantifier):
    __slosts__ = ()
    @property
    def value(self):
        return self._value() + '+'

class oneOrMoreLazy(BaseQuantifier):
    __slosts__ = ()
    @property
    def value(self):
        return self._value() + '+?'

 ### Literals
class anyChar(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '.'

class whitespaceChar(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\s'

class nonWhitespaceChar(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\S'

class Digit(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\d'

class nonDigit(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\D'

class Word(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\w'

class nonWord(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '\\W'

class Char(Base):
    __slosts__ = tuple(['_value'])
    def __init__(self, value):
        assert isinstance(value, str) and len(value) == 1
        super().__init__()
        self._value = scape_special(value)

    @property
    def value(self):
        return self._value

class rawChar(Base):
    __slosts__ = tuple(['_value'])
    def __init__(self, value):
        assert isinstance(value, str) and len(value) == 1
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

class String(Base):
    __slosts__ = tuple(['_values'])
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__(requiresGroup=True)
        self._values = scape_special(values)

    @property
    def value(self):
        return self._values

class rawString(Base):
    __slosts__ = tuple(['_values'])
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__(requiresGroup=True)
        self._values = values

    @property
    def value(self):
        return self._values

class Newline(Base):
    __slosts__ = ()

    @property
    def value(self):
        return '\\n'

class carriageReturn(Base):
    __slosts__ = ()

    @property
    def value(self):
        return '\\r'

class Tab(Base):
    __slosts__ = ()

    @property
    def value(self):
        return '\\t'

class Space(Base):
    __slosts__ = ()

    @property
    def value(self):
        return ' '

class Range(Base):
    __slosts__ = ('_begin', '_end', '_exclude', '_expression')
    def __init__(self, begin: Union[str, int], end: Union[str, int],
                 exclude: Optional[Union[List[Union[str, int]], str]]=None):
        super().__init__()
        tb = type(begin)
        # TODO: write explanations of asserts
        assert (isinstance(begin, str) and len(begin) == 1 and begin.isalpha()) or\
               (isinstance(begin, int) and 0 <= begin <= 9)
        assert (isinstance(end, str) and len(end) == 1 and begin.isalpha()) or\
               (isinstance(end, int) and 0 <= end <= 9)
        assert begin <= end
        assert str(begin).islower() == str(end).islower()
        if exclude:
            if isinstance(exclude, str):
                exclude = list(exclude)
            assert all([((isinstance(i, str) and len(i) == 1 and begin.isalpha()) or\
                   (isinstance(i, int) and 0 <= i <= 9)) and isinstance(i, tb) for i in exclude])
            exclude = list(sorted(exclude))
        self._begin = begin
        self._end = end
        self._exclude = exclude
        self._expression = ""
        if isinstance(begin, int):
            if exclude:
                self._expression = '['
                excludec = set(exclude)
                for i in range(begin, end+1):
                    if i in excludec:
                        continue
                    self._expression += str(i)
                self._expression += ']'
            else:
                self._expression = '['+str(begin)+'-'+str(end)+']'
        else:
            if exclude:
                excludec = set(exclude)
                self._expression = '['
                for i in range(ord(begin), ord(end)+1):
                    ch = chr(i)
                    if ch in excludec:
                        continue
                    self._expression += ch
                self._expression += ']'
            else:
                self._expression = '['+begin+'-'+end+']'

    @property
    def value(self):
        return self._expression

class anythingButRange(Base):
    __slosts__ = ('_begin', '_end', '_exclude', '_expression')
    def __init__(self, begin: Union[str, int], end: Union[str, int],
                 exclude: Optional[Union[List[Union[str, int]], str]]=None):
        super().__init__()
        tb = type(begin)
        # TODO: write explanations of asserts
        assert (isinstance(begin, str) and len(begin) == 1 and begin.isalpha()) or\
               (isinstance(begin, int) and 0 <= begin <= 9)
        assert (isinstance(end, str) and len(end) == 1 and begin.isalpha()) or\
               (isinstance(end, int) and 0 <= end <= 9)
        assert begin <= end
        assert str(begin).islower() == str(end).islower()
        if exclude:
            if isinstance(exclude, str):
                exclude = list(exclude)
            assert all([((isinstance(i, str) and len(i) == 1 and begin.isalpha()) or\
                   (isinstance(i, int) and 0 <= i <= 9)) and isinstance(i, tb) for i in exclude])
            exclude = list(sorted(exclude))
        self._begin = begin
        self._end = end
        self._exclude = exclude
        self._expression = ""
        if isinstance(begin, int):
            if exclude:
                self._expression = '[^'
                excludec = set(exclude)
                for i in range(begin, end+1):
                    if i in excludec:
                        continue
                    self._expression += str(i)
                self._expression += ']'
            else:
                self._expression = '[^'+str(begin)+'-'+str(end)+']'
        else:
            if exclude:
                excludec = set(exclude)
                self._expression = '[^'
                for i in range(ord(begin), ord(end)+1):
                    ch = chr(i)
                    if ch in excludec:
                        continue
                    self._expression += ch
                self._expression += ']'
            else:
                self._expression = '[^'+begin+'-'+end+']'

    @property
    def value(self):
        return self._expression


class anyOfChars(Base):
    __slosts__ = ('_values')
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__()
        self._values = scape_special(values)

    @property
    def value(self):
        return '['+self._values+']'

class anythingButChars(Base):
    __slosts__ = ('_values')
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__()
        self._values = scape_special(values)

    @property
    def value(self):
        return '[^'+self._values+']'
