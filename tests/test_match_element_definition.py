from expressive_regex import ExpressiveRegex
from expressive_regex import __version__


def test_version():
    assert __version__ == '0.1.0'

def test_anyChar():
    res=ExpressiveRegex()\
    .anyChar\
    .toRegexString()
    assert res=='.'