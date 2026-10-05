import sys

class TokenType:
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"

    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

    EOF = "EOF"

class Token:
    def __init__(self, kind, text, value, line):
        self.kind = kind
        self.text = text
        self.value = value
        self.line = line

    def __str__(self):
        return self.kind + " " + self.text + " " + str(self.value)

class Scanner:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.start = 0
        self.pos = 0
        self.line = 1

        self.words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def scan(self):
        while self.pos < len(self.code):
            self.start = self.pos
            self.scan_one()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_one(self):
        c = self.next_char()

        if c == "(":
            self.add(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add(TokenType.COMMA)
        elif c == ".":
            self.add(TokenType.DOT)
        elif c == "-":
            self.add(TokenType.MINUS)
        elif c == "+":
            self.add(TokenType.PLUS)
        elif c == ";":
            self.add(TokenType.SEMICOLON)
        elif c == "*":
            self.add(TokenType.STAR)

        elif c == "!":
            if self.check("="):
                self.add(TokenType.BANG_EQUAL)
            else:
                self.add(TokenType.BANG)

        elif c == "=":
            if self.check("="):
                self.add(TokenType.EQUAL_EQUAL)
            else:
                self.add(TokenType.EQUAL)

        elif c == ">":
            if self.check("="):
                self.add(TokenType.GREATER_EQUAL)
            else:
                self.add(TokenType.GREATER)

        elif c == "<":
            if self.check("="):
                self.add(TokenType.LESS_EQUAL)
            else:
                self.add(TokenType.LESS)

        elif c == "/":
            if self.check("/"):
                while self.peek() != "\n" and self.pos < len(self.code):
                    self.next_char()
            else:
                self.add(TokenType.SLASH)

        elif c == " " or c == "\t" or c == "\r":
            pass

        elif c == "\n":
            self.line += 1

        elif c == '"':
            self.get_string()

        elif self.is_number(c):
            self.get_number()

        elif self.is_letter(c):
            self.get_word()

        else:
            print("[line " + str(self.line) + "] Error: Unexpected character: " + c)

    def next_char(self):
        c = self.code[self.pos]
        self.pos += 1
        return c

    def add(self, kind, value=None):
        text = self.code[self.start:self.pos]
        self.tokens.append(Token(kind, text, value, self.line))

    def check(self, char):
        if self.pos >= len(self.code):
            return False

        if self.code[self.pos] != char:
            return False

        self.pos += 1
        return True

    def peek(self):
        if self.pos >= len(self.code):
            return "\0"

        return self.code[self.pos]

    def peek_next(self):
        if self.pos + 1 >= len(self.code):
            return "\0"

        return self.code[self.pos + 1]

    def get_string(self):
        while self.peek() != '"' and self.pos < len(self.code):
            if self.peek() == "\n":
                self.line += 1

            self.next_char()

        if self.pos >= len(self.code):
            print("[line " + str(self.line) + "] Error: Unterminated string.")
            return

        self.next_char()

        value = self.code[self.start + 1:self.pos - 1]
        self.add(TokenType.STRING, value)

    def get_number(self):
        while self.is_number(self.peek()):
            self.next_char()

        if self.peek() == "." and self.is_number(self.peek_next()):
            self.next_char()

            while self.is_number(self.peek()):
                self.next_char()

        text = self.code[self.start:self.pos]
        self.add(TokenType.NUMBER, float(text))

    def get_word(self):
        while self.is_letter_or_number(self.peek()):
            self.next_char()

        text = self.code[self.start:self.pos]

        if text in self.words:
            self.add(self.words[text])
        else:
            self.add(TokenType.IDENTIFIER)

    def is_number(self, c):
        return c >= "0" and c <= "9"

    def is_letter(self, c):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_letter_or_number(self, c):
        return self.is_letter(c) or self.is_number(c)

def run(src):
    scan = Scanner(src)
    tokens = scan.scan()

    for token in tokens:
        print(token)

def open_file(name):
    file = open(name, "r")
    src = file.read()
    file.close()
    run(src)

def run_prompt():
    while True:
        try:
            line = input("> ")
            run(line)
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break

def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py [script]")
    elif len(sys.argv) == 2:
        open_file(sys.argv[1])
    else:
        run_prompt()

main()