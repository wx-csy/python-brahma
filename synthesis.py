from sys import stderr
from typing import List, Tuple
import z3

from component import Component, std_lib
from program import Program

def _id_arr(prefix, num):
    return [f'{prefix}_{i}' for i in range(num)]

'''
5.1 Encoding Well-formed Programs
'''
def wfp_cons(lInput: List, lPR: List[Tuple], lOutput):
    cons = []

    # Appropriate Values
    nInput = len(lInput)
    nLib = len(lPR)
    for lParams, lRet in lPR:
        for lParam in lParams:
            cons.append(z3.And(0 <= lParam, lParam < nInput + nLib))
        cons.append(z3.And(nInput <= lRet, lRet < nInput + nLib))
    cons.append(z3.And(0 <= lOutput, lOutput < nInput + nLib))
    # Assign Fixed Value for lInput
    for i, lInp in enumerate(lInput) :
        cons.append(lInp == i)

    '''
    -   Consistency Constraint
    >   Every line in the program has at most one component.
    '''
    lRets = tuple(zip(*lPR))[1]
    for i in range(len(lRets)):
        for j in range(i):
            cons.append(lRets[i] != lRets[j])

    '''
    -   Acyclicity Constraint
    >   In a well-formed program, every variable is initialized *before* it is
    > used.
    '''
    for lParams, lRet in lPR:
        for lParam in lParams:
            cons.append(lParam < lRet)
    
    return z3.And(*cons)

'''
5.2 Encoding Dataflow in Programs
'''
def conn_cons(lInput: List, lPR: List[Tuple], lOutput, vInput: List, vPR: List[Tuple], vOutput):
    cons = []

    lList = lInput + [lOutput]
    for lParams, lRet in lPR:
        lList += lParams
        lList.append(lRet)
    
    vList = vInput + [vOutput]
    for vParams, vRet in vPR:
        vList += vParams
        vList.append(vRet)
    
    n = len(lList)
    assert n == len(vList)

    for i in range(n):
        for j in range(i):
            cons.append(z3.Implies(lList[i] == lList[j], vList[i] == vList[j]))
    
    return z3.And(*cons)

'''
    Encoding Library Constraint
'''
def lib_cons(vPR: List[Tuple], lib: List[Component]):
    cons = []
    for (vParam, vRet), comp in zip(vPR, lib):
        cons.append(vRet == comp.semantics(*vParam))
    return z3.And(*cons)

'''
    Encoding Specification Constraint
'''
def spec_cons(vInput: List, vOutput, spec):
    return spec(vOutput, *vInput)

'''
6   Synthesis Constraint Solving
'''
def synthesize(nInput, lib, spec):
    ctx = z3.Context()

    def make_loc_vars(prefix):
        lInput = list(z3.Ints(_id_arr(f'{prefix}_locInput', nInput), ctx))
        lPR = [
            (   
                list(z3.Ints(_id_arr(f'{prefix}_locParam_{i}', comp.arity), ctx)), 
                z3.Int(f'{prefix}_locReturn_{i}', ctx)
            ) for i, comp in enumerate(lib)
        ]
        lOutput = z3.Int(f'{prefix}_locOutput', ctx)
        return lInput, lPR, lOutput

    def make_value_vars(prefix):
        vInput = list(z3.BitVecs(_id_arr(f'{prefix}_valInput', nInput), 32, ctx))
        vPR = [
            (
                list(z3.BitVecs(_id_arr(f'{prefix}_valParam_{i}', comp.arity), 32, ctx)), 
                z3.BitVec(f'{prefix}_valReturn_{i}', 32, ctx)
            ) for i, comp in enumerate(lib)
        ]
        vOutput = z3.BitVec(f'{prefix}_valOutput', 32, ctx)
        return vInput, vPR, vOutput

    synthesizer = z3.Solver(ctx=ctx)
    verifier = z3.Solver(ctx=ctx)

    lInput, lPR, lOutput = make_loc_vars('cur')
    synthesizer.add(wfp_cons(lInput, lPR, lOutput))
    cevInput, cevPR, cevOutput = make_value_vars('ctr')
    verifier.add(conn_cons(lInput, lPR, lOutput, cevInput, cevPR, cevOutput))
    verifier.add(lib_cons(cevPR, lib))
    verifier.add(z3.Not(spec_cons(cevInput, cevOutput, spec)))
    
    '''
    ExAllSolver
    '''
    for iteration in range(100):
        print(f'> Running iteration #{iteration} ...')
        '''
        Step 1. Finite Synthesis
        >   In this step, we synthesize a design that works for finitely many
        > inputs. Specifically, the procedure finds values for L that work for
        > all the inputs in S.
        '''
        check_result = synthesizer.check()
        if check_result == z3.sat:
            syn_model = synthesizer.model()
            program = Program(nInput, syn_model, lPR, lOutput, lib)
            print(f'Finite synthesis success!')
            print(program)
        elif check_result == z3.unsat:
            '''
            >   If no such values are found, we terminate and declare that no
            > design could be found.
            '''
            print('not found')
            return None 
        else:
            print("don't know")
            return None

        '''
        Step 2. Verification
        >   In this step, we verify if the synthesized design - that we know
        > works for the inputs in S - also works for all inputs. Specifically, 
        > if the generated value currL for L works for all inputs, then we
        > terminate with success. If not, then we find an input on which it does
        > not work and add it to S.
        '''
        verifier.push()

        for lv in lInput:
            '''
              `model.eval(var, True)` is needed for model completion, since
            `model[var]` simply doesn't work for irrelavent variables. See
            https://github.com/Z3Prover/z3/issues/1920, it seems that Z3Py
            doesn't provide interface for enabling model completion globally.
            '''
            verifier.add(lv == syn_model.eval(lv, True))
        for lParams, lRet in lPR:
            for lParam in lParams:
                verifier.add(lParam == syn_model.eval(lParam, True))
            verifier.add(lRet == syn_model.eval(lRet, True))
        verifier.add(lOutput == syn_model.eval(lOutput, True))

        check_result = verifier.check()
        if check_result == z3.unsat:
            print('Verification passed!')
            return program
        elif check_result == z3.sat:
            print('Verification failed!')
            ver_model = verifier.model()
            cvInput, cvPR, cvOutput = make_value_vars(f'c{iteration}')
            synthesizer.add(lib_cons(cvPR, lib))
            synthesizer.add(conn_cons(lInput, lPR, lOutput, cvInput, cvPR, cvOutput))
            synthesizer.add(spec_cons(cvInput, cvOutput, spec))
            for cevI, cvI in zip(cevInput, cvInput) :
                synthesizer.add(cvI == ver_model.eval(cevI, True))
        else:
            return None

        verifier.pop()

    print('timeout')
    return None
