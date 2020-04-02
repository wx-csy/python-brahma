from abc import ABC, abstractmethod
from typing import List
from inspect import getargspec

import z3

'''
The abstract base class for base component specification.
'''
class Component(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.arity = len(getargspec(self.semantics)[0]) - 1
    
    @abstractmethod
    def semantics(self, *args):
        raise NotImplementedError

    @abstractmethod
    def expression(self, *args) -> str:
        raise NotImplementedError


class Add(Component):
    def __init__(self):
        super().__init__('add')

    def semantics(self, a, b):
        return a + b

    def expression(self, a, b) -> str:
        return f'{a} + {b}'


class Sub(Component):
    def __init__(self):
        super().__init__('sub')

    def semantics(self, a, b):
        return a - b

    def expression(self, a, b) -> str:
        return f'{a} - {b}'


class Neg(Component):
    def __init__(self):
        super().__init__('neg')

    def semantics(self, a):
        return -a 

    def expression(self, a) -> str:
        return f'-{a}'


class And(Component):
    def __init__(self):
        super().__init__('and')

    def semantics(self, a, b):
        return a & b

    def expression(self, a, b) -> str:
        return f'{a} & {b}'


class Or(Component):
    def __init__(self):
        super().__init__('or')

    def semantics(self, a, b):
        return a | b

    def expression(self, a, b) -> str:
        return f'{a} | {b}'

class Not(Component):
    def __init__(self):
        super().__init__('not')

    def semantics(self, a):
        return ~a

    def expression(self, a) -> str:
        return f'~{a}'

class Xor(Component):
    def __init__(self):
        super().__init__('xor')

    def semantics(self, a, b):
        return a ^ b

    def expression(self, a, b) -> str:
        return f'{a} ^ {b}'

class Constant(Component):
    def __init__(self, value):
        super().__init__(f'constant({value})')
        self.value = value

    def semantics(self):
        return self.value

    def expression(self) -> str:
        return f'{self.value}'

'''
7.3 Choice of Multi-set of Base Components

>   The standard library included 12 components, one each for performing 
> standard operations, such as bitwise-and, bitwise-or, bitwise-not, add-one,
> bitwise-xor, shift-right, comparison, add, and subtract operations.
'''

std_lib = [Add(), Sub(), Neg(), And(), Or(), Not(), Xor(), Constant(0), Constant(1)]

