# example - coroutil.py - decorator for priming coroutine

from functools import wraps

def coroutine(func):
    ''' decorator: primes 'func' by advancing to first 'yield' '''
    @wraps(func)
    # decorated generator function is replace by this primer function which, when invoked, returns the primed generator
    def primer(*args, **kwargs):
        # call the decorated function to get a generator object
        gen = func(*args, **kwargs)
        # prime the generator
        next(gen)
        # return it
        return gen
    return primer