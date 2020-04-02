from . import z3patch
from .synthesis import Synthesizer

if __name__ == '__main__':
    from z3 import And, Or, Implies
    import inspect
    print('Welcome to python-brahma. Type in a python function to specify the constraint.')
    print('E.g., `lambda y, a, b: y == a + b`')
    constraint = eval(input('>>> '))
    arity = len(inspect.getargspec(constraint)[0]) - 1
    synth = Synthesizer(arity, constraint)
    print(synth.synthesize())
