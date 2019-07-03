# example - code for an averager to continue that returns a result

from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0 
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            # in order to return a value, a coroutine must TERMINATE normally; this is why this version of averager has a condition to break out of its accumulating loop
            break
        total += term
        count += 1
        average = total/count
    # Return a namedtuple with the count and average. 
    return Result(count, average)

# # example - doctest showing the behavior of averager
# coro_avg = averager()
# next(coro_avg)
# # this version does not yield values
# coro_avg.send(10)
# coro_avg.send(30)
# coro_avg.send(6.5)
# # sending None terminates the loop, causing the coroutine to end by returning the result. As usual, the generator object raises StopIteration. The value attribute of the exception carries the value returned
# coro_avg.send(None)
# # Traceback (most recent call last):
# #   File "coroaverager2.py", line 28, in <module>
# #     coro_avg.send(None)
# # StopIteration: Result(count=3, average=15.5)

'''
Note: the value of the return expression is smuggled to the caller as an attribute of the StopIteration exception. 
    -Preserves the existing behavior of generator objects: raising StopIteration when exhausted
'''

# # example - Catching Stopiteration let's us get the value returned by averager
# coro_avg = averager()
# next(coro_avg)
# coro_avg.send(10)
# coro_avg.send(30)
# coro_avg.send(6.5)

# try:
#     coro_avg.send(None)
# except StopIteration as exc:
#     result = exc.value

# print(result)
# # Result(count=3, average=15.5)