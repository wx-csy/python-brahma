from abc import ABC, abstractmethod
from typing import List

import z3

'''
The abstract base class for base component specification.
'''
class component(ABC):
    def __init__(self, name: str, ctx: z3.Context = None) -> None:
        self.name = name
        self.context = ctx

    @property
    @abstractmethod
    def arity(self) -> int: 
        raise NotImplementedError
    
    @abstractmethod
    def semantics(self, *args):
        raise NotImplementedError

    @abstractmethod
    def expression(self, *args):
        raise NotImplementedError


class Add(component):
    def __init__(self):
        component.__init__(self, 'add')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a + b

    def expression(self, a, b):
        return f'{a} + {b}'


class Sub(component):
    def __init__(self):
        component.__init__(self, 'sub')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a - b

    def expression(self, a, b):
        return f'{a} - {b}'


class And(component):
    def __init__(self):
        component.__init__(self, 'and')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a & b

    def expression(self, a, b):
        return f'{a} & {b}'


class Or(component):
    def __init__(self):
        component.__init__(self, 'and')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a | b

    def expression(self, a, b):
        return f'{a} | {b}'


'''
7.3 Choice of Multi-set of Base Components

>   The standard library included 12 components, one each for performing 
> standard operations, such as bitwise-and, bitwise-or, bitwise-not, add-one,
> bitwise-xor, shift-right, comparison, add, and subtract operations.
'''

std_lib = [Add(), Sub(), And(), Or()]