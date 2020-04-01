from component import *

import z3

def format_program(nInput, model, lPR, lOutput, lib) :
    def id2name(id) :
        if id < nInput : 
            return f'x{id}'
        else :
            return f'v{id - nInput}'

    prog = [''] * len(lib)
    for (lParams, lRet), comp in zip(lPR, lib) :
        val = [model[lParam].as_long() for lParam in lParams]
        lRetVal = model[lRet].as_long()
        prog[lRetVal - nInput] = f"  v{lRetVal - nInput} = {comp.expression(*map(id2name, val))}"
    lOutputVal = model[lOutput].as_long()

    return f"def f({', '.join(map(id2name, range(nInput)))}) :" + '\n' + \
        '\n'.join(prog) + '\n' + f'  return {id2name(lOutputVal)}' + '\n'
