'''
Coroutines

"yield": to produce (generator objects) or to give way (context manager objects)

coroutines are a function with the yield keyword in its body BUT the "yield" usually appears on the right side of an expression instead of the left side (generator)
    -may or may not produce a value; if there is NO expression after the yield keyword, the generator will yield None
        ie. datum = yield
    -may receive data from the caller via .send(datum) instead of next(...)  

*possible that no data goes in or out through the "yield" keyword
**each coroutine yields control to a central scheduler so that other coroutines can be activated


How coroutines evolved from generators
"yield" & .send(value) 

using .send(...), the caller of the generator can post data which then becomes the value of the yield expression inside the generator function
    allows the generator to be used as a coroutine: a procedure that collaborates with the caller, yielding and receiving values from the caller

.send(), .throw(), .close()

Two syntax changes made to generator functions:
    1. A generator can now return a value; previously, providing a value to the return statement inside a generator raised SyntaxError
    2. The "yield from" syntax enables complex generators to be refactored into smaller, nested generators while avoiding a lot of boilerplate code previously required for a generator to delegate to subgenerators


Basic behavior of a generator used as a coroutine
Take a look at the example below
'''
# example - simplest possible demonstration of coroutine in action

# # a coroutine is defined as a generator function: with "yield" in its body on the right side instead of the left (if left then it is a generator)
# def simple_coroutine():
#     print('-> coroutine started!')
#     # "yield" is used in an expression; when the coroutine is designed just to receive data from the client it yields None - this is implicit as there is no expression to the right of the yield keyword
#     x = yield
#     print('-> coroutine received:', x)

# my_coro = simple_coroutine()
# # As usualy with generators, you call the function to get a generator object back
# print(my_coro)
# # <generator object simple_coroutine at 0x7f390fa024f8>

# # The first call is next(...) because the generator hasn't started so it's not waiting in a yield and we cant send it any data initially
# next(my_coro)
# # -> coroutine started!

# # This call makes the yield in the coroutine body evaluate to 42; now the coroutine resumes and runs until the next yield or termination
# my_coro.send(42)
# # -> coroutine received: 42
# # # In this case, control flows off the end of the coroutine body, which prompts the generator machinery to raise StopIteration, as usual
# # Traceback (most recent call last):
# #   File "Section16.py", line 44, in <module>
# #     my_coro.send(42)
# # StopIteration

'''
A coroutine can be in one of four states and you can determine the current state using the inspect.getgeneratorstate() function
    output:
        1. 'GEN_CREATED' - waiting to start execution
        2. 'GEN_RUNNING' - currently being executed by the interpreter
        3. 'GEN_SUSPENDED' - currently suspended at a yield expression
        4. 'GEN_CLOSED' - execution has completed

**argument to the .send() method will be come the value of the pending yield expression; a call like my_coro.send(42) only works if the coroutine is CURRENTLY SUSPENDED
    *need to activate FIRST before .send() (activation via next(my_coro) or my_coro.send(None))

The example below shows what happens when you immediately try to send it a value that is NOT None after being created
**initial next(my_coro) is referred to as "priming" the coroutine (advancing it to the first yield to make it ready for use as a LIVE coroutine)
'''

# example - attempting to send a value RIGHT after coroutine has been created
# coro_two = simple_coroutine()
# coro_two.send(1829) 
# # TypeError: can't send non-None value to a just-started generator

# # example - a coroutine that yields twice
# def simple_coro2(a):
#     print('-> Started: a =', a)
#     b = yield a
#     print('-> Received: b =', b)
#     c = yield a + b
#     print('-> Received: c =', c)

# my_coro2 = simple_coro2(14)
# from inspect import getgeneratorstate
# # inspect.getgeneratorstate reports GEN_CREATED, i.e. the coroutine has NOT started
# print(getgeneratorstate(my_coro2))
# # GEN_CREATED

# # Advance coroutine to first yield, printing -> Started: a = 14 message then yield value of a and suspending to wait for value to be assigned to b
# next(my_coro2)
# # -> Started: a = 14

# # getgeneratorstate reports GEN_SUSPENDED, i.e. the coroutine is paused at a yield expression
# print(getgeneratorstate(my_coro2))
# # GEN_SUSPENDED

# # Send number 28 to suspended coroutine; the yield expression evaluates to 28 and that number if bound to b. The -> Received: b = 28 message is displayed, the value of a + b is yielded (42) and the coroutine is suspended waiting for the value to be assigned to c
# print(my_coro2.send(28))
# # -> Received: b = 28
# # 42

# # Send number 99 to suspended coroutine; the yield expression evaluates to 99 the number is bound to c. The -> Received: c = 99 message is displayed then the coroutine TERMINATES, causing the generator object to raise StopIteration
# print(my_coro2.send(99))
# # -> Received: c = 99
# # Traceback (most recent call last):
# #   File "Section16.py", line 101, in <module>
# #     print(my_coro2.send(99))
# # StopIteration

# # getgeneratorstate reports GEN_CLOSED, i.e. the coroutine execution has COMPLETED
# print(getgeneratorstate(my_coro2))
# # GEN_SUSPENDED

'''
Crucial to understand that the execution of the coroutine is SUSPENDED exactly at the "yield" keyword
**in an assignment statement, the code to the right of the = is evaluated BEFORE the actual assignment happens
    ie. "b = yield a"
        the value of the b will ONLY be set when the coroutine is activated later by the client code

Execution of simple_coro2 coroutine can be split into THREE phases (take a look at figure 16-1 on pg. 495):
    1. next(my_coro2) prints first message and runs to yield a, yielding number 14;
    2. my_coro2.send(28) assigns 28 to b, prints second message and runs to yield a + b, yielding number 42
    3. my_coro2.send(99) assigns 99 to c, prints the third message and the coroutine terminates


Example: coroutine to compute a running average

*The advantage of using a coroutine is that total and count can be simple local variables: NO instance attributes or closures are needed to keep the context between calls
'''
# example - take a look at coroaverager0.py
# example - coroaverager0.py: doctest for the running average coroutine
# from Sec16_examples.coroaverager0 import averager

# # create the coroutine object
# coro_avg = averager()

# # prime the coroutine by calling next (no output because the initial value is set to None)
# next(coro_avg)

# # Now we are in business: each call to .send(...) yields the current average
# print(coro_avg.send(10))
# # 10.0
# print(coro_avg.send(30))
# # 20.0
# print(coro_avg.send(5))
# # 15.0


'''
Decorators for coroutine priming

Must always remember to call next(my_coro) before my_coro.send(x) (PRIME the coroutine)
    -to make it more convenient, a priming decorator is sometimes used

**the "yield from" syntax automatically primes the coroutine called by it, making it INCOMPATIBLE with decorators such as @coroutine
    **asyncio.coroutine decorator is designed to work with "yield from" so it does NOT prime the coroutine
'''
# example - take a look at coroutil.py
# example - take a look at coroaverager1.py


'''
Coroutine termination and exception handling

An unhandled exception within a coroutine propagates to the caller of the next or send which triggered it
'''
# example - how an unhandled exception kills a coroutine

# from Sec16_examples.coroaverager1 import averager
# coro_avg = averager()

# # using the @coroutine decorated averager we can immediately start sending values
# print(coro_avg.send(40))
# # 40.0

# print(coro_avg.send(50))
# # 45.0

# # Sending a non-numeric value causes an exception inside the coroutine
# print(coro_avg.send('spam'))
# # TypeError: unsupported operand type(s) for +=: 'float' and 'str'

# # Because the exception was NOT handled in the coroutine, it terminated. Any attempt to reactivate will raise StopIteration
# # program never reaches this line
# print(coro_avg.send(60))

'''
the example above shows that you can use .send() method with some sentinel value that tells the coroutine to exit
    ie. None, Ellipsis, StopIteration (class NOT instance) can all be sentinel values

Generator objects have TWO methods that allow the client to explicitly send exceptions into the coroutine - throw and close:
    generator.throw(exc_type[, exc_value[, traceback]])
        -causes the yield expression where the generator was paused to raise the exception given. if the exception is handled by the generator, flow advances to the next yield, and the value yielded becomes the value of the generator.throw call. If the exception is NOT handled by the generator, it propagates to the context of the caller.

    generator.close()
        -causes the yield expression where the generator was paused to raise a Generator Exit exception. No error is reported to the caller if the generator does NOT handle that exception or raises StopIteration - usually by running to completion. When receiving a GeneratorExit the generator must NOT yield a value, otherwise a RuntimeError is raised. If any other exception is raised by the generator, it propagates to the caller.
'''

# example - take a look at coro_exc_demo.py
# example - activating and closing with demo_exc_handling WITHOUT an exception
# from Sec16_examples.coro_exc_demo import demo_exc_handling
# exc_coro = demo_exc_handling()
# next(exc_coro)
# # -> coroutine started
# exc_coro.send(11)
# # -> coroutine received: 11
# exc_coro.send(22)
# # -> coroutine received: 22
# exc_coro.close()
# from inspect import getgeneratorstate
# print(getgeneratorstate(exc_coro))
# # GEN_CLOSED


# example - throwing DemoException into demo_exc_handling does NOT break it
# from Sec16_examples.coro_exc_demo import demo_exc_handling, DemoException
# from inspect import getgeneratorstate

# exc_coro = demo_exc_handling()
# next(exc_coro)
# # -> coroutine started
# exc_coro.send(11)
# # -> coroutine received: 11
# exc_coro.throw(DemoException)
# # *** DemoException handled. Continuing . . .
# print(getgeneratorstate(exc_coro))
# # GEN_SUSPENDED


# example - coroutine terminates if it CAN'T handle an exception throwin into it
# from Sec16_examples.coro_exc_demo import DemoException, demo_exc_handling
# from inspect import getgeneratorstate

# exc_coro = demo_exc_handling()
# next(exc_coro)
# # -> coroutine started
# exc_coro.send(11)
# -> coroutine received: 11
# exc_coro.throw(ZeroDivisionError)
# # Traceback (most recent call last):
# # ...
# # ZeroDivisionError
# print(getgeneratorstate(exc_coro))
# # GEN_SUSPENDED

'''
if it's necessary that some clean up code is run NO matter how the coroutine ends, you need to wrap the relevant part of the coroutine body in a try/finally block

**One of the main reasons why the "yield from" was added was to deal with throwing exceptions into nested coroutines. Another reason was to ENABLE coroutines to return values more conveniently . . . 
'''
# example - take a look at coro_finally_demo.py


'''
Returning a value from coroutine

the example below shows a variation of the averager coroutine that returns a result
    *doesn't yield anything - this shows that that some coroutines do NOT yield anything but are designed to return a value at the end (often a result of accumulation)
'''
# example - take a look at coroaverager2.py
# example - take a look at the 2nd part of coroaverager2.py
# example - take a look at the 3rd part of coroaverager2.py


'''
Using yield from

when a generator gen calls "yield from subgen()", the subgen takes over and will yield values to the caller of gen; the caller will in effect drive subgen directly. Meanwhile gen will be blocked, waiting until subgen terminates
'''
# # example - yield from used as a shortcut for nested for loops
# def gen():
#     for c in 'AB':
#         yield c
#     for i in range(1, 3):
#         yield i
# print(list(gen()))
# # ['A', 'B', 1, 2]

# # the function above can be written as the function below

# def gen_one():
#     yield from 'AB'
#     yield from range(1, 3)
# print(list(gen_one()))
# # ['A', 'B', 1, 2]

# # example - Chaining iterables with yield from
# def chain(*iterables):
#     for it in iterables:
#         yield from it

# s = 'ABC'
# t = tuple(range(3))
# print(list(chain(s, t)))
# # ['A', 'B', 'C', 0, 1, 2]

'''
the main feature of "yield from" is to open a BIDIRECTIONAL channel from the outermost caller to the innermost subgenerator, so that values can be sent and yielded back and forth directly from them and exceptions can be thrown all the way in without adding a lot of exception handling boilerplate code in the intermediate coroutines

delegating generator
    -the generator function that contains the yield from <iterable> expression

subgenerator
    -the generator obtained from the <iterable> part of the yield from expression

caller
    -to refer to the client code that calls the delegating generator

**take a look at figure 16-2 for a picture representation
'''
# example - take a look at coroaverager3.py

