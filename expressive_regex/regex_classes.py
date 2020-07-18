import abc
from typing import Union, Optional, List

class Base(metaclass=abc.ABCMeta):
    __slosts__= ()
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError

class BaseGroups(Base, metaclass=abc.ABCMeta):

    __slosts__ = ('_elements')
    def __init__(self, elements):
        self._elements = elements

    @classmethod
    def element(self, cls, elements):
        return cls(elements)

class Root(BaseGroups):
    __slosts__= ()
    def value(self):
        pass

class Group(BaseGroups):
    __slosts__= ()
    def value(self):
        pass



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

    def value(self):
        pass