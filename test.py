import time
import inspect

import z3
from z3 import And, Or, Implies, If
from brahma import Synthesizer


test_cases = [
    lambda y, a: y == a & (a - 1),
    lambda y, a: y == a & (a + 1),
    lambda y, a: y == a & -a,
    lambda y, a: y == a ^ (a - 1),
    lambda y, a: y == a | (a - 1),

    lambda y, a: y == a | (a + 1),
    lambda y, a: y == (~a) & (a + 1),
    lambda y, a: y == (~a) & (a - 1),
    lambda y, a: y == If(a >= 0, a, -a),
    lambda y, a: If(a > 0, y == 1, If(a < 0, y == -1, y == 0)),
]

'''
int sign(int x) {
    return -x >> 31 | -(x >> 31);
}
'''

for i, cons in enumerate(test_cases):
    print(f'Synthesizing #{i+1} ...')
    arity = len(inspect.getargspec(cons)[0]) - 1
    synth = Synthesizer(arity, cons)

    program = None
    length = None
    while True:
        try :
            t0 = time.clock()
            newprog = synth.synthesize(max_len=length)
            if newprog is None: break
            program = newprog
            length = program.sloc - 1
            print(f'Current length = {program.sloc}')
            print(program)
            print('%.2f seconds used.' % (time.clock() - t0))
        except TimeoutException as ex:
            print('Execution timeout.')
