class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Grouping:
    def __init__(self, expression):
        self.expression = expression


class Literal:
    def __init__(self, value):
        self.value = value