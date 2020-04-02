import z3

__old_z3_And = z3.And
z3.And = lambda *args : __old_z3_And(*args, args[0].ctx)

__old_z3_Or = z3.Or
z3.Or  = lambda *args : __old_z3_Or (*args, args[0].ctx)
