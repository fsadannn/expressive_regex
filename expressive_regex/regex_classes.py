import abc
from typing import Union, Optional, List
import copy
from .exceptions import BadStatement

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
class Base(metaclass=abc.ABCMeta):
    __slosts__ = ('_requiresGroup')
    def __init__(self, requiresGroup=False):
        self._requiresGroup = requiresGroup

    @property
    def isOneCharLiteral(self):
        return False

    @property
    def isLiteral(self):
        return False

    @property
    def isNegatedLiteral(self):
        return False

    @property
    def requiresGroup(self):
        return self._requiresGroup

    @abc.abstractproperty
    def value(self): # pragma: no cover
        raise NotImplementedError

    def copy(self): # pragma: no cover
        return copy.deepcopy(self)

class Literal(Base, metaclass=abc.ABCMeta):
    @property
    def isLiteral(self):
        return True

class NegatedLiteral(Literal, metaclass=abc.ABCMeta):
    __slosts__ = ()
    @property
    def isNegatedLiteral(self):
        return True

class OneCharLiteral(Literal, metaclass=abc.ABCMeta):
    __slosts__ = ()
    @property
    def isOneCharLiteral(self):
        return True

class BaseGroups(Base, metaclass=abc.ABCMeta):
    __slosts__ = ('_elements')
    def __init__(self, elements):
        super().__init__()
        self._elements = elements

    @classmethod
    def element(cls, elements): # pragma: no cover
        return cls(elements)


class BaseQuantifier(BaseGroups, metaclass=abc.ABCMeta):
    __slosts__ = ()
    def __init__(self, element):
        assert not isinstance(element, (list, tuple))
        super().__init__(element)

    def _value(self):
        inner = self._elements.value
        verif = not(len(inner) == 1 or (len(inner) == 2 and '\\' in inner))
        grouping = f"(?:{inner})" if self._elements.requiresGroup and verif else inner
        return grouping

### Grouping
class Root(BaseGroups):
    __slosts__ = ()
    @property
    def value(self):
        return "".join((i.value for i in self._elements))

class SetOfLiterals(BaseGroups):
    __slosts__ = ()
    def __init__(self, elements):
        super().__init__(elements)
        # the next line work but is imposible report properly the error make by the user
        # assert all(map(lambda x: x.isLiteral and not x.isNegatedLiteral ,elements))
        for x in elements:
            if not x.isLiteral or x.isNegatedLiteral:
                raise BadStatement(f'type {type(x)} isn\'t admited inside "setOfLiterals"')

    @property
    def value(self):
        res = "["
        for i in self._elements:
            value = i.value
            if not i.isOneCharLiteral:
                value = value[1:-1]
            res += value
        res += "]"
        return res

class Capture(BaseGroups):
    __slosts__ = ()
    @property
    def value(self):
        return "("+"".join((i.value for i in self._elements))+")"

class Group(BaseGroups):
    __slosts__ = ()
    @property
    def value(self):
        return "(?:"+"".join((i.value for i in self._elements))+")"

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

class Between(BaseQuantifier):
    __slosts__ = ('_a', '_b')
    def __init__(self, element, a: int, b: int):
        assert isinstance(a, int) and isinstance(b, int), "Between params must be int"
        assert 0 <= a <= b
        super().__init__(element)
        self._a = str(a)
        self._b = str(b)

    @property
    def value(self):
        if self._a == '0':
            if self._b == '1':
                return self._value() + '?'
            return self._value() + '{,' + self._b + '}'
        return self._value() + '{' + self._a + ',' + self._b + '}'

class betweenLazy(BaseQuantifier):
    __slosts__ = ('_a', '_b')
    def __init__(self, element, a: int, b: int):
        assert isinstance(a, int) and isinstance(b, int), "betweenLazy params must be int"
        assert 0 <= a <= b
        super().__init__(element)
        self._a = str(a)
        self._b = str(b)

    @property
    def value(self):
        return self._value() + '{' + self._a + ',' + self._b + '}?'

class Exactly(BaseQuantifier):
    __slosts__ = ('_a')
    def __init__(self, element, a: int):
        assert isinstance(a, int), "Exactly param must be int"
        assert a > 0
        super().__init__(element)
        self._a = str(a)

    @property
    def value(self):
        return self._value() + '{' + self._a + '}'

class atLeast(BaseQuantifier):
    __slosts__ = ('_a')
    def __init__(self, element, a: int):
        assert isinstance(a, int), "Exactly param must be int"
        assert a >= 0
        super().__init__(element)
        self._a = str(a)

    @property
    def value(self):
        if self._a == '0':
            return self._value() + '*'
        if self._a == '1':
            return self._value() + '+'
        return self._value() + '{' + self._a + ',}'

class upTo(BaseQuantifier):
    __slosts__ = ('_b')
    def __init__(self, element, b: int):
        assert isinstance(b, int), "Exactly param must be int"
        assert b > 0
        super().__init__(element)
        self._b = str(b)

    @property
    def value(self):
        if self._b == '1':
            return self._value() + '?'
        return self._value() + '{,' + self._b + '}'

 ### Literals
class anyChar(Base):
    __slosts__ = ()
    @property
    def value(self):
        return '.'

class whitespaceChar(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\s'

class nonWhitespaceChar(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\S'

class Digit(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\d'

class nonDigit(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\D'

class Word(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\w'

class nonWord(OneCharLiteral):
    __slosts__ = ()
    @property
    def value(self):
        return '\\W'

class Char(OneCharLiteral):
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

class Newline(OneCharLiteral):
    __slosts__ = ()

    @property
    def value(self):
        return '\\n'

class carriageReturn(OneCharLiteral):
    __slosts__ = ()

    @property
    def value(self):
        return '\\r'

class Tab(OneCharLiteral):
    __slosts__ = ()

    @property
    def value(self):
        return '\\t'

class Space(OneCharLiteral):
    __slosts__ = ()

    @property
    def value(self):
        return ' '

class Range(Literal):
    __slosts__ = ('_begin', '_end', '_exclude', '_expression')
    def __init__(self, begin: Union[str, int], end: Union[str, int],
                 exclude: Optional[Union[List[Union[str, int]], str]]=None):
        super().__init__()
        tb = type(begin)
        # TODO: write explanations of asserts
        assert (isinstance(begin, str) and len(begin) == 1 and begin.isalnum()) or\
               (isinstance(begin, int) and 0 <= begin <= 9)
        assert (isinstance(end, str) and len(end) == 1 and begin.isalnum()) or\
               (isinstance(end, int) and 0 <= end <= 9)
        assert begin <= end
        assert str(begin).islower() == str(end).islower()
        assert str(begin).isnumeric() == str(end).isnumeric()
        if exclude:
            if isinstance(exclude, str):
                exclude = list(exclude)
            assert all([((isinstance(i, str) and len(i) == 1 and begin.isalnum()) or\
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

class anythingButRange(NegatedLiteral):
    __slosts__ = ('_begin', '_end', '_exclude', '_expression')
    def __init__(self, begin: Union[str, int], end: Union[str, int],
                 exclude: Optional[Union[List[Union[str, int]], str]]=None):
        super().__init__()
        tb = type(begin)
        # TODO: write explanations of asserts
        assert (isinstance(begin, str) and len(begin) == 1 and begin.isalnum()) or\
               (isinstance(begin, int) and 0 <= begin <= 9)
        assert (isinstance(end, str) and len(end) == 1 and begin.isalnum()) or\
               (isinstance(end, int) and 0 <= end <= 9)
        assert begin <= end
        assert str(begin).islower() == str(end).islower()
        assert str(begin).isnumeric() == str(end).isnumeric()
        if exclude:
            if isinstance(exclude, str):
                exclude = list(exclude)
            assert all([((isinstance(i, str) and len(i) == 1 and begin.isalnum()) or\
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


class anyOfChars(Literal):
    __slosts__ = ('_values')
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__()
        self._values = scape_special(values)

    @property
    def value(self):
        return '['+self._values+']'

class anythingButChars(NegatedLiteral):
    __slosts__ = ('_values')
    def __init__(self, values):
        assert isinstance(values, str)
        super().__init__()
        self._values = scape_special(values)

    @property
    def value(self):
        return '[^'+self._values+']'
