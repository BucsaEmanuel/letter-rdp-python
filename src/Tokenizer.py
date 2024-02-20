import re

Spec = [
    # ----------------
    # WHITESPACE
    [r"^\s+", None],

    # ----------------
    # COMMENTS
    # Skip single-line comments:
    [r"^\/\/.*", None],
    # Skip multi-line comments:
    [r"^\/\*[\s\S]*?\*\/", None],

    # ----------------
    # Symbols, delimiters:
    [r"^;", ';'],
    [r"^\{", '{'],
    [r"^\}", '}'],
    [r"^\(", '('],
    [r"^\)", ')'],
    [r"^,", ','],
    [r"^\.", '.'],
    [r"^\[", '['],
    [r"^\]", ']'],

    # ----------------
    # Keywords:
    [r"^\blet\b", 'let'],
    [r"^\bif\b", 'if'],
    [r"^\belse\b", 'else'],
    [r"^\btrue\b", 'true'],
    [r"^\bfalse\b", 'false'],
    [r"^\bnull\b", 'null'],
    [r"^\bwhile\b", 'while'],
    [r"^\bdo\b", 'do'],
    [r"^\bfor\b", 'for'],
    [r"^\bdef\b", 'def'],
    [r"^\breturn\b", 'return'],
    [r"^\bclass\b", 'class'],
    [r"^\bextends\b", 'extends'],
    [r"^\bsuper\b", 'super'],
    [r"^\bnew\b", 'new'],
    [r"^\bthis\b", 'this'],

    # ----------------
    # NUMBERS
    [r"^\d+", 'NUMBER'],

    # ----------------
    # Identifiers:
    [r"^\w+", "IDENTIFIER"],

    # ----------------
    # Equality operators: ==, !=
    [r"^[=!]=", "EQUALITY_OPERATOR"],

    # ----------------
    # Assignment operators =, *=, /=, +=, -=
    [r"^=", "SIMPLE_ASSIGN"],
    [r"^[\*\/\+\-]=", "COMPLEX_ASSIGN"],

    # ----------------
    # Math operators: +, -, *, /
    [r"^[+\-]", "ADDITIVE_OPERATOR"],
    [r"^[*\/]", "MULTIPLICATIVE_OPERATOR"],

    # ----------------
    # Relational operators: >, >=, <, <=
    [r"^[><]=?", "RELATIONAL_OPERATOR"],

    # ----------------
    # Logical operators: &&, ||
    [r"^&&", "LOGICAL_AND"],
    [r"^\|\|", "LOGICAL_OR"],
    [r"^!", "LOGICAL_NOT"],

    # ----------------
    # STRINGS
    [r'"[^"]*"', 'STRING'],
    [r"'[^']*'", 'STRING'],
]


class Tokenizer:

    def init(self, string):
        self._string = string
        self._cursor = 0

    def isEOF(self):
        """
        Whether the tokenizer reached EOF.
        :return:
        """
        return self._cursor == len(self._string)

    def hasMoreTokens(self):
        return self._cursor < len(self._string)

    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        string = self._string[self._cursor:]

        for regexp, tokenType in Spec:
            tokenValue = self._match(regexp, string)

            # Couldn't match this rule, continue.
            if tokenValue is None:
                continue

            # Should skip token, e.g. whitespace.
            if tokenType is None:
                return self.getNextToken()

            return {
                "type": tokenType,
                "value": tokenValue
            }
        raise SyntaxError(f"Unexpected token: \"{string[0]}\"")

    def _match(self, regexp, string):
        matched = re.match(regexp, string)
        if not matched:
            return None
        self._cursor += len(matched.group(0))
        return matched.group(0)
