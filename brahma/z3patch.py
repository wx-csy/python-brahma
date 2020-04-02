import z3

_old_And = z3.And
z3.And = lambda *args: _old_And(*args, args[0].ctx)

_old_Or = z3.Or
z3.Or = lambda *args: _old_Or(*args, args[0].ctx)