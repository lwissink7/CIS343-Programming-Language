from ast_nodes import Binary, Unary, Grouping, Literal, PrintStmt, ExprStmt


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def parse(self):
        statements = []

        while not self.is_end():
            try:
                statements.append(self.statement())
            except ParseError:
                self.synchronize()

        return statements

    def statement(self):
        if self.match(["PRINT"]):
            expr = self.expression()
            self.consume("SEMICOLON", "Expected ';' after print statement.")
            return PrintStmt(expr)

        expr = self.expression()
        self.consume("SEMICOLON", "Expected ';' after expression.")
        return ExprStmt(expr)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(["BANG_EQUAL", "EQUAL_EQUAL"]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator.text, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(["GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"]):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator.text, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(["MINUS", "PLUS"]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator.text, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(["SLASH", "STAR"]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator.text, right)

        return expr

    def unary(self):
        if self.match(["BANG", "MINUS"]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator.text, right)

        return self.primary()

    def primary(self):
        if self.match(["FALSE"]):
            return Literal(False)

        if self.match(["TRUE"]):
            return Literal(True)

        if self.match(["NIL"]):
            return Literal(None)

        if self.match(["NUMBER", "STRING"]):
            return Literal(self.previous().value)

        if self.match(["LEFT_PAREN"]):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expected ')' after expression.")
            return Grouping(expr)

        if self.is_end():
            self.error(self.peek(), "Expected expression.")
        else:
            self.error(self.peek(), "Unexpected token: " + self.peek().text)

    def consume(self, kind, message):
        if self.match([kind]):
            return self.previous()

        self.error(self.peek(), message)

    def synchronize(self):
        while not self.is_end():
            if self.current > 0 and self.previous().kind == "SEMICOLON":
                return

            if self.peek().kind == "PRINT":
                return

            self.advance()

    def match(self, kinds):
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True

        return False

    def check(self, kind):
        if self.is_end():
            return False

        return self.peek().kind == kind

    def advance(self):
        if not self.is_end():
            self.current += 1

        return self.previous()

    def is_end(self):
        return self.peek().kind == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        print("[line " + str(token.line) + "] Error: " + message)
        self.had_error = True
        raise ParseError()
