from abc import ABC, abstractmethod
from typing import List
from inspect import getargspec

import z3

'''
The abstract base class for base component specification.
'''
class Component(ABC):
    def __init__(self, name: str, ctx) -> None:
        self.name = name
        self.arity = len(getargspec(self.semantics)[0]) - 1
        self.ctx = ctx
    
    @abstractmethod
    def semantics(self, *args):
        raise NotImplementedError

    @abstractmethod
    def expression(self, *args, model) -> str:
        raise NotImplementedError

    def parameters(self):
        return ()


class Add(Component):
    def __init__(self, ctx):
        super().__init__('add', ctx)

    def semantics(self, a, b):
        return a + b

    def expression(self, a, b, model) -> str:
        return f'{a} + {b}'


class Sub(Component):
    def __init__(self, ctx):
        super().__init__('sub', ctx)

    def semantics(self, a, b):
        return a - b

    def expression(self, a, b, model) -> str:
        return f'{a} - {b}'


class Inc(Component):
    def __init__(self, ctx):
        super().__init__('inc', ctx)

    def semantics(self, a):
        return a + 1

    def expression(self, a, model) -> str:
        return f'{a} + 1'


class Dec(Component):
    def __init__(self, ctx):
        super().__init__('dec', ctx)

    def semantics(self, a):
        return a - 1

    def expression(self, a, model) -> str:
        return f'{a} - 1'


class Neg(Component):
    def __init__(self, ctx):
        super().__init__('neg', ctx)

    def semantics(self, a):
        return -a 

    def expression(self, a, model) -> str:
        return f'-{a}'


class And(Component):
    def __init__(self, ctx):
        super().__init__('and', ctx)

    def semantics(self, a, b):
        return a & b

    def expression(self, a, b, model) -> str:
        return f'{a} & {b}'


class Or(Component):
    def __init__(self, ctx):
        super().__init__('or', ctx)

    def semantics(self, a, b):
        return a | b

    def expression(self, a, b, model) -> str:
        return f'{a} | {b}'


class Not(Component):
    def __init__(self, ctx):
        super().__init__('not', ctx)

    def semantics(self, a):
        return ~a

    def expression(self, a, model) -> str:
        return f'~{a}'


class Xor(Component):
    def __init__(self, ctx):
        super().__init__('xor', ctx)

    def semantics(self, a, b):
        return a ^ b

    def expression(self, a, b, model) -> str:
        return f'{a} ^ {b}'
    

class SignBit(Component):
    def __init__(self, ctx):
        super().__init__('signbit', ctx)

    def semantics(self, a):
        return a >> 31

    def expression(self, a, model) -> str:
        return f'{a} >> 31'


class Constant(Component):
    def __init__(self, value, ctx):
        super().__init__(f'const({value})', ctx)
        self.value = value

    def semantics(self):
        return self.value

    def expression(self, model) -> str:
        return f'{self.value}'


class VaradicConstant(Component):
    def __init__(self, ctx):
        super().__init__(f'varconst', ctx)
        self.value = z3.BitVec(f'varconst_{id(self)}', 32, ctx=self.ctx)

    def semantics(self):
        return self.value

    def expression(self, model) -> str:
        return f'{model.eval(self.value, True)}'

    def parameters(self):
        return (self.value,)

'''
7.3 Choice of Multi-set of Base Components

>   The standard library included 12 components, one each for performing 
> standard operations, such as bitwise-and, bitwise-or, bitwise-not, add-one,
> bitwise-xor, shift-right, comparison, add, and subtract operations.
'''
def std_lib(ctx) :
    return [
        Add(ctx),
        Sub(ctx),
        Neg(ctx),
        Inc(ctx),
        Dec(ctx),
        And(ctx),
        Or(ctx),
        Not(ctx),
        Xor(ctx),
        SignBit(ctx),
        Constant(1, ctx),
        VaradicConstant(ctx),
    ]
