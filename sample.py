import brahma
import z3

synth = brahma.Synthesizer(2, lambda y, a, b: z3.And(z3.UGE(y, a), z3.UGE(y, b)))
synth.synthesize()