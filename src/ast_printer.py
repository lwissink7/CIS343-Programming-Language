from ast_nodes import Binary, Unary, Grouping, Literal


class AstPrinter:
    def print(self, expr):
        return self.get_expr(expr)

    def get_expr(self, expr):
        if isinstance(expr, Binary):
            return self.binary(expr)
        elif isinstance(expr, Unary):
            return self.unary(expr)
        elif isinstance(expr, Grouping):
            return self.grouping(expr)
        elif isinstance(expr, Literal):
            return self.literal(expr)

    def binary(self, expr):
        return "(" + expr.operator + " " + self.get_expr(expr.left) + " " + self.get_expr(expr.right) + ")"

    def unary(self, expr):
        return "(" + expr.operator + " " + self.get_expr(expr.right) + ")"

    def grouping(self, expr):
        return "(group " + self.get_expr(expr.expression) + ")"

    def literal(self, expr):
        if expr.value is None:
            return "nil"
        elif expr.value == True:
            return "true"
        elif expr.value == False:
            return "false"
        else:
            return str(expr.value)