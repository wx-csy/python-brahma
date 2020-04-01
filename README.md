# python-brahma

This is a Python implementation of *Brahma*, using [Z3](https://github.com/Z3Prover/z3) as the Satisfiability Modulo Theory (SMT) solver.

Brahma (Synthesis of Loop-free Programs, PLDI'11, Sumit Gulwani et al) is a simple loop-free program synthesizer. It can be used to synthesize several straight-line programs. The most famous applications are discovering bit-manipulation tricks, as described in *Hacker's Delight*, commonly referred to as the Bible of bit twiddling hacks.

## Example

To turn-off the rightmost 1 bit, the *Brahma* synthesizer may give the following program:
``` python
def f(x0):
    v1 = -x0
    v3 = x0 & v1
    return v3 
```

## Usage

Type `python3 brahma.py` in terminal to enter interactive mode:

```
Welcome to python-brahma. Type in a python function to specify the constraint.
E.g., `lambda y, a, b: y == a + b`
>>> 
```

Then type in a python lambda expression. The first argument is the return value,
and the others are the arguments of the function to synthesize. Return a Boolean
expression denoting the constraint on the input and output.

## Requirement
- Python 3.6 or above

- Z3 (with Python API)
  
  You can install it with the following script:

  ```
  # works on ubuntu
  sudo apt install libz3-dev
  ```
  
  

