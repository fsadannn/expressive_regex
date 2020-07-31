from expressive_regex import ExpressiveRegex
from expressive_regex.regex_classes import specialChars
from expressive_regex import __version__
import string
import random


def test_version():
    assert __version__ == '0.4.4'

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

def test_newline():
    res=ExpressiveRegex()\
    .newline\
    .toRegexString()
    assert res=='\\n'

def test_carriageReturn():
    res=ExpressiveRegex()\
    .carriageReturn\
    .toRegexString()
    assert res=='\\r'

def test_tab():
    res=ExpressiveRegex()\
    .tab\
    .toRegexString()
    assert res=='\\t'

def test_space():
    res=ExpressiveRegex()\
    .space\
    .toRegexString()
    assert res==' '

def test_char_and_rawChar():
    for i in string.ascii_letters:
        res=ExpressiveRegex()\
        .char(i)\
        .toRegexString()
        assert res==i
        res=ExpressiveRegex()\
        .rawChar(i)\
        .toRegexString()
        assert res==i
    for i in string.digits:
        res=ExpressiveRegex()\
        .char(i)\
        .toRegexString()
        assert res==i
        res=ExpressiveRegex()\
        .rawChar(i)\
        .toRegexString()
        assert res==i
    for i in specialChars:
        res=ExpressiveRegex()\
        .char(i)\
        .toRegexString()
        assert res=='\\'+i
        res=ExpressiveRegex()\
        .rawChar(i)\
        .toRegexString()
        assert res==i

def test_string_and_rawString():
    expression = "".join(random.choices(string.ascii_letters, k=random.randint(1,len(string.ascii_letters))))
    res=ExpressiveRegex()\
        .string(expression)\
        .toRegexString()
    assert res==expression
    res=ExpressiveRegex()\
        .rawString(expression)\
        .toRegexString()
    assert res==expression
    expression = "".join(random.choices(specialChars, k=random.randint(1,len(specialChars))))
    fix_expression = "".join(('\\'+i for i in expression))
    res=ExpressiveRegex()\
        .string(expression)\
        .toRegexString()
    assert res==fix_expression
    res=ExpressiveRegex()\
        .rawString(expression)\
        .toRegexString()
    assert res==expression

def test_range():
    exp=ExpressiveRegex()\
        .range(0,9)\
        .toRegex()
    for d in string.digits:
        res = exp.search(d)
        assert res is not None
    exclud = [2]
    exp=ExpressiveRegex()\
        .range(0,9, exclude=exclud)\
        .toRegex()
    for d in string.digits:
        res = exp.search(d)
        if int(d) in exclud:
            assert res is None
        else:
            assert res is not None
    exclud = [2,4]
    exp=ExpressiveRegex()\
        .range(0,9, exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.digits:
        res = exp.search(d)
        if int(d) in exclud:
            assert res is None
        else:
            assert res is not None
    exp=ExpressiveRegex()\
        .range('a','z')\
        .toRegex()
    for d in string.ascii_lowercase:
        res = exp.search(d)
        assert res is not None
    exclud = 'a'
    exp=ExpressiveRegex()\
        .range('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is None
        else:
            assert res is not None
    exclud = 'abz'
    exp=ExpressiveRegex()\
        .range('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is None
        else:
            assert res is not None
    exclud = 'a'
    exp=ExpressiveRegex()\
        .range('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is None
        else:
            assert res is not None
    exclud = 'AFX'
    exp=ExpressiveRegex()\
        .range('A','Z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_uppercase:
        res = exp.search(d)
        if d in exclud:
            assert res is None
        else:
            assert res is not None

def test_anythingButRange():
    exp=ExpressiveRegex()\
        .anythingButRange(0,9)\
        .toRegex()
    for d in string.digits:
        res = exp.search(d)
        assert res is None
    exclud = [2]
    exp=ExpressiveRegex()\
        .anythingButRange(0,9, exclude=exclud)\
        .toRegex()
    for d in string.digits:
        res = exp.search(d)
        if int(d) in exclud:
            assert res is not None
        else:
            assert res is None
    exclud = [2,4]
    exp=ExpressiveRegex()\
        .anythingButRange(0,9, exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.digits:
        res = exp.search(d)
        if int(d) in exclud:
            assert res is not None
        else:
            assert res is None
    exp=ExpressiveRegex()\
        .anythingButRange('a','z')\
        .toRegex()
    for d in string.ascii_lowercase:
        res = exp.search(d)
        assert res is None
    exclud = 'a'
    exp=ExpressiveRegex()\
        .anythingButRange('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is not None
        else:
            assert res is None
    exclud = 'abz'
    exp=ExpressiveRegex()\
        .anythingButRange('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is not None
        else:
            assert res is None
    exclud = 'a'
    exp=ExpressiveRegex()\
        .anythingButRange('a','z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_lowercase:
        res = exp.search(d)
        if d in exclud:
            assert res is not None
        else:
            assert res is None
    exclud = 'AFX'
    exp=ExpressiveRegex()\
        .anythingButRange('A','Z', exclude=exclud)\
        .toRegex()
    exclud = set(exclud)
    for d in string.ascii_uppercase:
        res = exp.search(d)
        if d in exclud:
            assert res is not None
        else:
            assert res is None

def test_anyOfChars():
    expression = "".join(random.choices(string.ascii_letters, k=random.randint(1,len(string.ascii_letters))))
    res=ExpressiveRegex()\
        .anyOfChars(expression)\
        .toRegexString()
    assert res=='['+expression+']'

def test_anythingButChars():
    expression = "".join(random.choices(string.ascii_letters, k=random.randint(1,len(string.ascii_letters))))
    res=ExpressiveRegex()\
        .anythingButChars(expression)\
        .toRegexString()
    assert res=='[^'+expression+']'




