# Grouping

## .group

Creates a non-capturing group of the proceeding elements. Needs to be finalised with `.end()`.

**Example**

```Python
ExpressiveRegex()\
    .group\
        .range('a', 'f')\
        .range('0', '9')\
        .string('XXX')\
    .end()\
.toRegexString()
```

```Python
([a-f][0-9]XXX)
```

## .capture

Creates a capture group for the proceeding elements. Needs to be finalised with `.end()`.

**Example**

```Python
ExpressiveRegex()\
    .capture\
        .range('a', 'f')\
        .range('0', '9')\
        .string('XXX')\
    .end()\
.toRegexString()
```

```Python
([a-f][0-9]XXX)
```

## .setOfLiterals

Creates a set from the proceeding elements. Needs to be finalised with `.end()`.
Inside this statement only is allowed [Literals](../literals/#literals) except
[anyChar](../literals/#anychar), [.rawChar](../literals/#rawcharc),
[.string](../literals/#strings), [.rawString](../literals/#rawstrings),
[.anythingButRange](../literals/#anythingbutrangea-b-exclude),
[.anythingButChars](../literals/#anythingbutcharschars)

**Example**

```Python
ExpressiveRegex()\
    .setOfLiterals\
        .char('-')\
        .range(1,4)\
        .anyOfChars('dfs')\
    .end()\
.toRegexString()
```

```Python
"[\-1-4dfs]"
```

### .end()

Signifies the end of a ExpressiveRegex grouping.

**Example**

```Python
ExpressiveRegex()
    .capture\
        .setOfLiterals\
            .char('-')\
            .range(1,4)\
            .anyOfChars('dfs')\
        .end()\
        .range('0', '9')\
        .string('XXX')\
    .end()\
.toRegexString()
```

```Python
([\-1-4dfs][0-9]XXX)
```
