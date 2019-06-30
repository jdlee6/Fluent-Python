# example - aritprog_v3.py: this works like the previous aritprog_gen functions
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n:n<end, ap_gen)
        return ap_gen

'''
NOT a generator function (has no yield in its body) but still returns a generator SO it operates as a generator factory just like how a generator function does

*When implementing generators; KNOW what is available in the standard library so you are NOT reinventing the wheel
'''
