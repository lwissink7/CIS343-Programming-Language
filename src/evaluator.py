from ast_nodes import Binary, Unary, Grouping, Literal, Variable, Assign, PrintStmt, ExprStmt, VarStmt, BlockStmt


class Evaluator:
    def __init__(self):
        self.scopes = [{}]

    def execute(self, stmt):
        if isinstance(stmt, PrintStmt):
            value = self.evaluate(stmt.expression)
            print(self.print_value(value))

        elif isinstance(stmt, ExprStmt):
            self.evaluate(stmt.expression)

        elif isinstance(stmt, VarStmt):
            scope = self.scopes[-1]
            name = stmt.name.text

            if name in scope:
                raise ValueError("[line " + str(stmt.name.line) + "] Variable already declared: " + name)

            value = None
            if stmt.initializer is not None:
                value = self.evaluate(stmt.initializer)

            scope[name] = value

        elif isinstance(stmt, BlockStmt):
            self.scopes.append({})

            try:
                for item in stmt.statements:
                    self.execute(item)
            finally:
                self.scopes.pop()

    def get_variable(self, token):
        for scope in reversed(self.scopes):
            if token.text in scope:
                return scope[token.text]

        raise ValueError("[line " + str(token.line) + "] Undefined variable: " + token.text)

    def set_variable(self, token, value):
        for scope in reversed(self.scopes):
            if token.text in scope:
                scope[token.text] = value
                return value

        raise ValueError("[line " + str(token.line) + "] Undefined variable: " + token.text)

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)

        elif isinstance(expr, Variable):
            return self.get_variable(expr.name)

        elif isinstance(expr, Assign):
            value = self.evaluate(expr.value)
            return self.set_variable(expr.name, value)

        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)

            if expr.operator == "!":
                return not self.is_true(right)
            elif expr.operator == "-":
                return -self.to_number(right)

        elif isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator == "+":
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return self.to_number(left) + self.to_number(right)
            elif expr.operator == "-":
                return self.to_number(left) - self.to_number(right)
            elif expr.operator == "*":
                return self.to_number(left) * self.to_number(right)
            elif expr.operator == "/":
                right = self.to_number(right)
                if right == 0:
                    raise ValueError("Division by zero.")
                return self.to_number(left) / right
            elif expr.operator == ">":
                return self.to_number(left) > self.to_number(right)
            elif expr.operator == ">=":
                return self.to_number(left) >= self.to_number(right)
            elif expr.operator == "<":
                return self.to_number(left) < self.to_number(right)
            elif expr.operator == "<=":
                return self.to_number(left) <= self.to_number(right)
            elif expr.operator == "==":
                return left == right
            elif expr.operator == "!=":
                return left != right

    def is_true(self, value):
        if value is None:
            return False
        if value is False:
            return False
        if isinstance(value, (int, float)) and value == 0:
            return False
        return True

    def to_number(self, value):
        if value is True:
            return 1
        if value is False:
            return 0
        if isinstance(value, (int, float)):
            return value
        raise ValueError("Invalid number.")

    def print_value(self, value):
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "nil"
        return str(value)
