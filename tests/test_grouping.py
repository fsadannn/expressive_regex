from expressive_regex import ExpressiveRegex

def test_setOfLiterals():
    res=ExpressiveRegex()\
    .setOfLiterals\
    .char('-')\
    .range(1,4)\
    .anyOfChars('dfs')\
    .end()\
    .toRegexString()
    assert res=='[\\-1-4dfs]'


def test_group():
    res=ExpressiveRegex()\
    .group\
    .setOfLiterals\
    .char('-')\
    .range(1,4)\
    .anyOfChars('dfs')\
    .end()\
    .end()\
    .toRegexString()
    assert res=='(?:[\\-1-4dfs])'

def test_capture():
    res=ExpressiveRegex()\
    .capture\
    .setOfLiterals\
    .char('-')\
    .range(1,4)\
    .anyOfChars('dfs')\
    .end()\
    .end()\
    .toRegexString()
    assert res=='([\\-1-4dfs])'