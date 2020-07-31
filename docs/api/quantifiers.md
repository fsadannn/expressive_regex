# Quantifiers

## .optional

Matches `0` or `1` of the proceeding expression.

**Example**

```Python
ExpressiveRegex()\
.optional.digit\
.toRegexString()
```

```Python
"\d?"
```

## .zeroOrMore

Matches `0` or `more` repetitions of the proceeding expression.

**Example**

```Python
ExpressiveRegex()\
.zeroOrMore.digit\
.toRegexString()
```

```Python
"\d*"
```

## .zeroOrMoreLazy

Matches `0` or `more` repetitions of the proceeding expression, but as few times as possible.

**Example**

```Python
ExpressiveRegex()\
.zeroOrMoreLazy.digit\
.toRegexString()
```

```Python
"\d*"
```

## .oneOrMore

Matches `1` or `more` repetitions of the proceeding expression.

**Example**

```Python
ExpressiveRegex()\
.oneOrMore.digit\
.toRegexString()
```

```Python
"\d+"
```

## .oneOrMoreLazy

Matches `1` or `more` repetitions of the proceeding expression, but as few times as possible.

**Example**

```Python
ExpressiveRegex()\
.oneOrMoreLazy.digit\
.toRegexString()
```

```Python
"\d+?"
```

## .exactly(n)

Matches exactly `n` repetitions of the proceeding expression.

**Example**

```Python
ExpressiveRegex()\
.exactly(4).digit\
.toRegexString()
```

```Python
"\d{4}"
```

## .atLeast(n)

Matches at least `n` repetitions of the proceeding expression.
If `n` is `1` then is equivalente to [.oneOrMore](#oneormore) .
If `n` is `0` then is equivalente to [.zeroOrMore](#zeroormore) .

**Example**

```Python
ExpressiveRegex()\
.atLeast(4).digit\
.toRegexString()
```

```Python
"\d{4,}"
```

## .uoTo(n)

Matches up to `n` repetitions of the proceeding expression.
If `n` is `1` then is equivalente to [.optional](#optional) .

**Example**

```Python
ExpressiveRegex()\
.uoTo(4).digit\
.toRegexString()
```

```Python
"\d{,4}"
```

## .between(n,m)

Matches between `n` and `m` repetitions of the proceeding expression.
If `n` is `0` and `m` is `1` then is equivalente to [.optional](#optional) .
If `n` is `0` and `m` > `1` then is equivalente to [.uoTo(m)](#uoton) .

**Example**

```Python
ExpressiveRegex()\
.between(2,4).digit\
.toRegexString()
```

```Python
"\d{2,4}"
```

## .betweenLazy(n,m)

Matches between `n` and `m` repetitions of the proceeding expression, but as few times as possible.

**Example**

```Python
ExpressiveRegex()\
.between(2,4).digit\
.toRegexString()
```

```Python
"\d{2,4}?"
```
