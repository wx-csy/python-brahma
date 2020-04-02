import brahma
import z3

synth = brahma.Synthesizer(2, lambda y, a, b: y == a + 2 * b)
print(synth.synthesize_shortest())