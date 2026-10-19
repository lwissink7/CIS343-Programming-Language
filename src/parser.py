from ast_nodes import Binary, Unary, Grouping, Literal


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def parse(self):
        expr = self.expression()

        if self.had_error:
            return None

        if not self.is_end():
            token = self.peek()
            self.error(token, "Unexpected token after expression: " + token.text)
            return None

        return expr

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

            if not self.match(["RIGHT_PAREN"]):
                self.error(self.peek(), "Expected ')' after expression.")

            return Grouping(expr)

        token = self.peek()

        if token.kind == "EOF":
            self.error(token, "Expected expression.")
        else:
            self.error(token, "Unexpected token: " + token.text)

        return None

    def match(self, kinds):
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True

        return False

    def check(self, kind):
        if self.is_end():
            return kind == "EOF"

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