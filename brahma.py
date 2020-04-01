#!/usr/bin/env python3

import inspect
from synthesizer import synthesize
from component import std_lib

def main():
    print('Welcome to python-brahma. Type in a python function to specify the constraint.')
    print('E.g., `lambda y, a, b: y == a + b`')
    constraint = eval(input('>>> '))
    arity = len(inspect.getargspec(constraint)[0]) - 1
    print(synthesize(arity, std_lib, constraint))

if __name__ == '__main__':
    main()