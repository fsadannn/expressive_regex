# Expressive Regex

<img alt="PyPI - License" src="https://img.shields.io/github/license/fsadannn/expressive_regex"> <img alt="PyPI - License" src="https://travis-ci.org/fsadannn/expressive_regex.svg"> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fsadannn/expressive_regex.svg">

This project was made with inspiration from [Super Expressive for JavaScript](https://github.com/francisrstokes/super-expressive).

Expressive Regex allow you to build regular expressions in almost natural language and without external dependency.

[Documentation](https://fsadannn.github.io/expressive_regex/)

**Example**
to match a telephone number that can be in the format 555-555-555, 555 555 555 or 555555555.

```Python
ExpressiveRegex()\
    .exactly(2).group\
        .oneOrMore.digit\
        .optional.setOfLiterals\
            .char('-')\
            .whitespaceChar\
        .end()\
    .end()\
    .oneOrMore.digit\
.toRegexString()
```

```Python
"(?:\d+[\-\s]?){2}\d+"
```