from expressive_regex import ExpressiveRegex

def test_optional():
    res=ExpressiveRegex()\
    .optional.digit\
    .toRegexString()
    assert res=='\\d?'

def test_zeroOrMore():
    res=ExpressiveRegex()\
    .zeroOrMore.digit\
    .toRegexString()
    assert res=='\\d*'

def test_zeroOrMoreLazy():
    res=ExpressiveRegex()\
    .zeroOrMoreLazy.digit\
    .toRegexString()
    assert res=='\\d*?'

def test_oneOrMore():
    res=ExpressiveRegex()\
    .oneOrMore.digit\
    .toRegexString()
    assert res=='\\d+'

def test_oneOrMoreLazy():
    res=ExpressiveRegex()\
    .oneOrMoreLazy.digit\
    .toRegexString()
    assert res=='\\d+?'

def test_exactly():
    res=ExpressiveRegex()\
    .exactly(4).digit\
    .toRegexString()
    assert res=='\\d{4}'

def test_atLeast():
    res=ExpressiveRegex()\
    .atLeast(4).digit\
    .toRegexString()
    assert res=='\\d{4,}'
    res=ExpressiveRegex()\
    .atLeast(0).digit\
    .toRegexString()
    assert res=='\\d*'
    res=ExpressiveRegex()\
    .atLeast(1).digit\
    .toRegexString()
    assert res=='\\d+'

def test_upTo():
    res=ExpressiveRegex()\
    .upTo(4).digit\
    .toRegexString()
    assert res=='\\d{,4}'
    res=ExpressiveRegex()\
    .upTo(1).digit\
    .toRegexString()
    assert res=='\\d?'

def test_between():
    res=ExpressiveRegex()\
    .between(2,4).digit\
    .toRegexString()
    assert res=='\\d{2,4}'
    res=ExpressiveRegex()\
    .between(0,1).digit\
    .toRegexString()
    assert res=='\\d?'
    res=ExpressiveRegex()\
    .between(0,4).digit\
    .toRegexString()
    assert res=='\\d{,4}'

def test_betweenLazy():
    res=ExpressiveRegex()\
    .betweenLazy(2,4).digit\
    .toRegexString()
    assert res=='\\d{2,4}?'