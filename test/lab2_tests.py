from ast_nodes import Binary, Unary, Grouping, Literal
from ast_printer import AstPrinter


printer = AstPrinter()


test1 = Binary(
    Unary("-", Literal(10)),
    "+",
    Grouping(
        Binary(
            Literal(5),
            "*",
            Binary(Literal(8), "/", Literal(2))
        )
    )
)

print("Test 1:")
print(printer.print(test1))
print()


test2 = Binary(
    Binary(
        Binary(Literal(10), ">", Literal(5)),
        "==",
        Literal(True)
    ),
    "!=",
    Binary(
        Unary("!", Literal(False)),
        "==",
        Binary(Literal(4), "<=", Literal(6))
    )
)

print("Test 2:")
print(printer.print(test2))
print()


test3 = Binary(
    Binary(
        Binary(Literal(10), "-", Literal(3)),
        ">=",
        Binary(Literal(2), "<", Literal(5))
    ),
    "==",
    Grouping(
        Binary(Literal("hello"), "==", Literal(None))
    )
)

print("Test 3:")
print(printer.print(test3))