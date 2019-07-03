# example - coroaverager1.py: doctest and code for a running average coroutine using the @coroutine decorator

from inspect import getgeneratorstate

# import the coroutine decorator
from Sec16_examples.coroutil import coroutine

# apply it to the averager function
@coroutine
# the body of the function is exactly the same as the averager() function in coroaverager0.py
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
    
# Call averager(), creating a generator object that is primed inside the primer function of the coroutine decorator
coro_avg = averager()

# # getgeneratorstate reports GEN_SUSPENDED, meaning that the coroutine is ready to receive a value
# print(getgeneratorstate(coro_avg))
# # GEN_SUSPENDED

# # You can immediately start SENDING values to coro_avg: that's the point of the decorator (to make it ready without calling next(my_coro) to prime it)
# print(coro_avg.send(10))
# # 10.0
# print(coro_avg.send(30))
# # 20.0
# print(coro_avg.send(5))
# # 15.0