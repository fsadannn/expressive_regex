# Literals

Literals are the simplest form of pattern matching in regular expressions. They will simply succeed whenever that literal is found.

## .anyChar

Matches any character except a newline.

**Example**

```Python
ExpressiveRegex()\
.anyChar\
.toRegexString()
```

```Python
"."
```

## .whitespaceChar

Matches any whitespace character; equivalent to `[ \t\n\r\f\v]`.
 In Unicode it will match the whole range of Unicode whitespace characters.

**Example**

```Python
SuperExpressive()\
.whitespaceChar\
.toRegexString()
```

```Python
"\s"
```

## .nonWhitespaceChar

Matches any non-whitespace character; equivalent to `[^\s]`.

**Example**

```Python
SuperExpressive()\
.nonWhitespaceChar\
.toRegexString()
```

```Python
"\S"
```

## .digit

Matches any non-whitespace character; equivalent to `[0-9]`.
 In Unicode it will match the whole range of Unicode digits.

**Example**

```Python
SuperExpressive()\
.digit\
.toRegexString()
```

```Python
"\d"
```

## .nonDigit

 Matches any non-digit character; equivalent to `[^\d]`.

**Example**

```Python
SuperExpressive()\
.nonDigit\
.toRegexString()
```

```Python
"\D"
```

## .word

Matches any alpha-numeric (`a-z, A-Z, 0-9`) characters, as well as `_`.
In Unicode it will match the range of Unicode alphanumeric characters
(letters plus digits plus underscore).

**Example**

```Python
SuperExpressive()\
.word\
.toRegexString()
```

```Python
"\w"
```

## .nonWord

Matches any non alpha-numeric (`a-z, A-Z, 0-9`) characters, excluding `_` as well.

**Example**

```Python
SuperExpressive()\
.nonWord\
.toRegexString()
```

```Python
"\W"
```

## .newline

Matches a `\n` character.

**Example**

```Python
SuperExpressive()\
.newline\
.toRegexString()
```

```Python
"\n"
```

## .carriageReturn

Matches a `\r` character.

**Example**

```Python
SuperExpressive()\
.carriageReturn\
.toRegexString()
```

```Python
"\r"
```

## .tab

Matches a `\t` character.

**Example**

```Python
SuperExpressive()\
.tab\
.toRegexString()
```

```Python
"\t"
```

## .space

Matches a ` ` character.

**Example**

```Python
SuperExpressive()\
.space\
.toRegexString()
```

```Python
" "
```

## .char(c)

Matches the exact char `c` but scape special characters `('\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-')`.

**Examples**

```Python
SuperExpressive()\
.char('a')\
.toRegexString()
```

```Python
"a"
```

```Python
SuperExpressive()\
.char('$')\
.toRegexString()
```

```Python
"\$"
```

## .rawChar(c)

Matches the exact char `c` and don't scape special characters.

**Examples**

```Python
SuperExpressive()\
.rawChar('a')\
.toRegexString()
```

```Python
"a"
```

```Python
SuperExpressive()\
.rawChar('$')\
.toRegexString()
```

```Python
"$"
```

## .string(s)

Matches the exact string `s` but scape special characters `('\', '.', '^', '$', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}', '-')`.

**Example**

```Python
SuperExpressive()\
.string('2$')\
.toRegexString()
```

```Python
"2\$"
```

## .rawString(c)

Matches the exact string `s` and don't scape special characters.

**Example**

```Python
SuperExpressive()\
.string('2$')\
.toRegexString()
```

```Python
"2$"
```

## .range(a, b, exclude)

Matches any character that falls between `a` and `b` and don't mathch character
in the exclude set. `a` and `b` must be same type, `a`<=`b` and:

- if `"a"`<=`a`<=`"z"` then `"a"`<=`b`<=`"z"`
- if `"A"`<=`a`<=`"Z"` then `"A"`<=`b`<=`"A"`
- if `"0"`<=`a`<=`"9"` then `"0"`<=`b`<=`"9"`
- if `0`<=`a`<=`9` then `0`<=`b`<=`9`

`exclude` must be an string or list or tuple of single char string. By default exclude is `None`

**Examples**

```Python
SuperExpressive()\
.range('a','f')\
.toRegexString()
```

```Python
"[a-f]"
```

```Python
SuperExpressive()\
.range('a','f', exclude='bd')\
.toRegexString()
```

```Python
"[acef]"
```

```Python
SuperExpressive()\
.range('a','f', exclude=['b','d'])\
.toRegexString()
```

```Python
"[acef]"
```

## .anythingButRange(a, b, exclude)

Matches any character, except those that would be captured by the [.range](#rangea-b-exclude).

**Examples**

```Python
SuperExpressive()\
.anythingButRange('a','f')\
.toRegexString()
```

```Python
"[^a-f]"
```

```Python
SuperExpressive()\
.anythingButRange('a','f', exclude='bd')\
.toRegexString()
```

```Python
"[^acef]"
```

## .anyOfChars(chars)

Matches any of the characters in the provided string `chars` and scape special characters.

**Example**

```Python
SuperExpressive()\
.anyOfChars('abd$')\
.toRegexString()
```

```Python
"[abd\$]"
```

## .anythingButChars(chars)

Matches any character, except any of those in the provided string `chars` and scape special characters.

**Example**

```Python
SuperExpressive()\
.anythingButChars('abd$')\
.toRegexString()
```

```Python
"[^abd\$]"
```
