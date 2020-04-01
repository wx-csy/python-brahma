from abc import ABC, abstractmethod
from typing import List
import z3

'''
The abstract base class for base component specification.
'''
class Component(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    @abstractmethod
    def arity(self) -> int: 
        raise NotImplementedError
    
    @abstractmethod
    def semantics(self, *args):
        raise NotImplementedError

    @abstractmethod
    def expression(self, *args) -> str:
        raise NotImplementedError


class Add(Component):
    def __init__(self):
        Component.__init__(self, 'add')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a + b

    def expression(self, a, b) -> str:
        return f'{a} + {b}'


class Sub(Component):
    def __init__(self):
        Component.__init__(self, 'sub')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a - b

    def expression(self, a, b) -> str:
        return f'{a} - {b}'


class Neg(Component):
    def __init__(self):
        Component.__init__(self, 'neg')
    
    @property
    def arity(self) -> int:
        return 1

    def semantics(self, a):
        return -a 

    def expression(self, a) -> str:
        return f'-{a}'


class And(Component):
    def __init__(self):
        Component.__init__(self, 'and')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a & b

    def expression(self, a, b) -> str:
        return f'{a} & {b}'


class Or(Component):
    def __init__(self):
        Component.__init__(self, 'and')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a | b

    def expression(self, a, b) -> str:
        return f'{a} | {b}'

class Not(Component):
    def __init__(self):
        Component.__init__(self, 'not')
    
    @property
    def arity(self) -> int:
        return 1

    def semantics(self, a):
        return ~a

    def expression(self, a) -> str:
        return f'~{a}'

class Xor(Component):
    def __init__(self):
        Component.__init__(self, 'xor')
    
    @property
    def arity(self) -> int:
        return 2

    def semantics(self, a, b):
        return a ^ b

    def expression(self, a, b) -> str:
        return f'{a} ^ {b}'

class Constant(Component):
    def __init__(self, value):
        Component.__init__(self, f'constant({value})')
        self.value = value
    
    @property
    def arity(self) -> int:
        return 0

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

std_lib = [Add(), Sub(), Neg(), And(), Or(), Not(), Xor(), Constant(1)]