import z3

__old_And = z3.And
z3.And = lambda *args: __old_And(*args, args[0].ctx)

__old_Or = z3.Or
z3.Or = lambda *args: __old_Or(*args, args[0].ctx)
