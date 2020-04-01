from typing import List
import z3

from component import Component

class Instruction:
    def __init__(self, component: Component, args: List) -> None:
        self.reached = False
        self.component = component
        self.args = args

class Program:
    def __id2name(self, id: int) -> str:
        if id < self.nInput: 
            return f'x{id}'
        else :
            return f'v{id - self.nInput}'

    def __init__(self, nInput, model, lPR, lOutput, lib) -> None:
        self.nInput = nInput
        self.lOutput = model[lOutput].as_long()

        instrs = [None] * len(lib)
        for (lParams, lRet), comp in zip(lPR, lib):
            lParamVals = [model[lParam].as_long() for lParam in lParams]
            lRetVal = model[lRet].as_long()
            instrs[lRetVal - nInput] = Instruction(comp, lParamVals)
        self.instructions = instrs
        
        '''
        Dead Code Removal

        3   Problem Definition
        >   We note that the implementation above is using *all* components
        > from the library. We can assume this without any loss of generality.
        > Even when there is a correct implementation using fewer components,
        > that implementation can always be extended to an implementation that
        > uses all components by adding dead code. Dead code can be easily
        > identified and removed in a post-processing step.
        '''
        def visiting(id):
            if id < nInput: return
            instr = instrs[id - nInput]
            if instr.reached: return
            for sid in instr.args: 
                visiting(sid)
            instr.reached = True
        
        visiting(self.lOutput)
        
    def __repr__(self) -> str:
        prog = [f"def f({', '.join(map(self.__id2name, range(self.nInput)))}):"]
        for id, instr in enumerate(self.instructions):
            if instr.reached :
                prog.append(f'    v{id} = ' + instr.component.expression(*map(self.__id2name, instr.args)))
        prog.append(f'    return {self.__id2name(self.lOutput)}')
        return '\n'.join(prog) + '\n'
