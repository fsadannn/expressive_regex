from expressive_regex import ExpressiveRegex
from expressive_regex import __version__


def test_version():
    assert __version__ == '0.1.0'

def test_anyChar():
    res=ExpressiveRegex()\
    .anyChar\
    .toRegexString()
    assert res=='.'

def test_whitespaceChar():
    res=ExpressiveRegex()\
    .whitespaceChar\
    .toRegexString()
    assert res=='\\s'

def test_nonWhitespaceChar():
    res=ExpressiveRegex()\
    .nonWhitespaceChar\
    .toRegexString()
    assert res=='\\S'

def test_digit():
    res=ExpressiveRegex()\
    .digit\
    .toRegexString()
    assert res=='\\d'

def test_nonDigit():
    res=ExpressiveRegex()\
    .nonDigit\
    .toRegexString()
    assert res=='\\D'

def test_word():
    res=ExpressiveRegex()\
    .word\
    .toRegexString()
    assert res=='\\w'

def test_nonWord():
    res=ExpressiveRegex()\
    .nonWord\
    .toRegexString()
    assert res=='\\W'