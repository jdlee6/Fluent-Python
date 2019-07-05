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

**argument to the .send() method will become the value of the pending yield expression; a call like my_coro.send(42) only works if the coroutine is CURRENTLY SUSPENDED
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
# # GEN_CLOSED

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
# # GEN_CLOSED

'''
if it's necessary that some clean up code is run NO matter how the coroutine ends, you need to wrap the relevant part of the coroutine body in a try/finally block

**One of the main reasons why the "yield from" was added was to deal with throwing exceptions into nested coroutines. Another reason was to ENABLE coroutines to return values more conveniently . . . 
'''


# example - take a look at coro_finally_demo.py


'''
Returning a value from coroutine

the example below shows a variation of the averager coroutine that returns a result
    *doesn't yield anything - this shows that some coroutines do NOT yield anything but are designed to return a value at the end (often a result of accumulation)
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

# example - take a look at coroaverager3.py and take a look at the overview description at the bottom


'''
The meaning of "yield from"
'''
# example - simplified pseudocode equivalent to the statement RESULT = yield from EXPR in the delegating generator
#  .throw() and .close() are NOT supported; the only exception handled is StopIteration
# EXPR - can be any iterable

# # the EXPR can be any iterable, because iter() is applied to get an iterator _i (this is the subgenerator)
# _i = iter(EXPR)
# try:
#     # the subgenerator is primed; the result is stored to be the first yielded value _y
#     _y = next(_i)
# except StopIteration as _e:
#     # If StopIteration was raised, extract the value attribute from the exception and assign it to _r: this is the RESULT in the simplest case
#     _r = _e.value
# else:
#     # While this loop is running, the delegating generator is blocked, operating just as a channel between the caller and the subgenerator
#     while 1:
#         # yield the current item yielded from the subgenerator; wait for a value _s sent by the caller. Note that this is the only yield in this listing
#         _s = yield _y
#         try:
#             # try to advance the subgenerator, forwarding the _s sent by the caller
#             _y = _i.send(s)
#         # If the subgenerator raised StopIteration, get the value, assign to _r and exit the loop, resuming the delegating generator    
#         except StopIteration as _e:
#             _r = _e.value
#             break

# # _r is the RESULT: the value of the whole yield from expression
# RESULT = _r

'''
_i (iterator)
_y (yielded)
_r (result)
_s (sent)
_e (exception)

if the subgenerator implements .throw()/.close(); this must be handled by the "yield from" logic
if the subgenerator implements those methods, inside the subgenerator BOTH methods cause exceptions to be raised, which must be handled by the "yield from"
the subgenerator may also throw exceptions of its own, unprovoked by the caller, and this must also be dealt with in the "yield from"
*if the caller calls next() or .send(None), both are forwarded as a next() call on the subgenerator; only if the caller sends a non-None value, the .send() method of the subgenerator is used

Look at the pseudocode below
'''
# # the EXPR can be any iterable, because iter() is applied to get an iterator _i (this is the subgenerator)
# _i = iter(EXPR)
# try:
#     # the subgenerator is primed; the result is stored to be the first yielded value _y
#     _y = next(_i)
# except StopIteration as e:
#     # If StopIteration was raised, extract the value attribute from the exception and assign to _r: this is the RESULT in the simplest case
#     _r = _e.value
# else:
#     # While this loop is running, the delegating generator is blocked, operating just as a channel between the caller and the subgenerator
#     while 1:
#         try:
#             # Yield the current item yielded from the subgenerator; wait for a value _s sent by the caller. This is the only yield in this listing
#             _s = yield _y
#         # This deals with closing the delegating generator and the subgenerator. Since the subgenerator can be any iterator, it may not have a close method
#         except GeneratorExit as _e:
#             try:
#                 _m = _i.close
#             except AttributeError:
#                 pass
#             else:
#                 m()
#             raise _e
#         # This deals with exceptions thrown in by the caller using .throw(...). Again, the subgenerator may be an iterator with no throw method to be called - in which case the exception is raised in the delegating generator
#         except BaseException as _e:
#             _x = sys.exc_info()
#             try:
#                 _m = _i.throw
#             except AttributeError:
#                 raise _e
#             # If the subgenerator has a throw method, call it with the exception passed from the caller. The subgenerator may handle the exception (and the loop continues); it may raise StopIteration (the _r result is extracted from it and the loop ends); or it may raise the same or another exception which is not handled here and propagates to the delegating generator
#             else:
#                 try:
#                     _y = _m(*_x)
#                 except StopIteration as _e:
#                     _r = _e.value
#                     break
#         # if no exception was received when yielding ...
#         else:
#             # try to advance the subgenerator ...
#             try:
#                 # call next on the subgenerator if the last value received from the caller was None, otherwise call send
#                 if _s is None:
#                     _y = next(_i)
#                 else:
#                     _y = _i.send(s)
#             # if the subgenerator raised StopIteration, get the value, assign to _r and exit the loop, resuming the delegating generator
#             except StopIteration as _e:
#                 _r = _e.value
#                 break
# # _r is the RESULT: the value of the whole yield from expression
# RESULT = _r

'''
!Important!
***find the "while", the "yield", the "next", and the .send() calls: these will help you get an idea of how the whole structure works
*because the subgenerator is primed, an auto-priming decorator is INCOMPATIBLE with yield from

the reason why we are looking at pseudocode is because that most real life examples tend to associate themselves with asyncio module (they depend on an active event loop to work)


Use case (programming simulations): coroutines for discrete event simulation 
*does NOT implement yield from but reveals how coroutines are used to manage concurrent activities on a single thread

coroutines are the fundamental building block of the asyncio module
a simulation shows how to implement concurrent (events occuring at the same time) activities using coroutines instead of threads 


About discrete event simulations
DES is a type of simulation where a system is modeled as a sequence of events
    -simulation "clock" does NOT advance by fixed increments, but advances directly to the simulated time of the next modeled event

DES is NOT a continuous simulation (which is when the clock advances continuously by a fixed - and usually small - increment)

think of a DES like a turn based game: state of the game only moves when a play moves, while the player is choosing which move to make the game is frozen


The taxi fleet simulation
take a look at taxi_sim.py
'''

# # example: testing taxi_process [test this in the terminal and not in vs code]
# from Sec16_examples.taxi_sim import taxi_process

# # create a generator object to represent a taxi with ident=13 that will make two trips and start working at t=0
# taxi = taxi_process(ident=13, trips=2, start_time=0)

# # prime the coroutine; it yields the initial event
# next(taxi)
# # Event(time=0, proc=13, action='leave garage')

# # we can now send it the current time. In the console, the _ variable is bound to the last result; here I add 7 to the time, which means the taxi will spend 7 minutes searching for the first passenger
# taxi.send(_.time + 7)
# # Event(time=7, proc=13, action='pick up passenger')

# # Sending _.time + 23 means the trip with the first passenger will last 23 minutes
# taxi.send(_.time + 23)
# # Event(time=30, proc=13, action='drop off passenger')

# # then the taxi will prowl for 5 minutes
# taxi.send(_.time + 5)
# # Event(time=35, proc=13, action='pick up passenger')

# # the last trip will take 48 minutes
# taxi.send(_.time + 48)
# # Event(time=83, proc=13, action='drop off passenger')

# taxi.send(_.time + 1)
# # After two complete trips. the loop ends and the 'going home' event is yielded
# # Event(time=84, proc=13, action='going home')

# # The next attempt to send to the coroutine causes it to fall through the end. When it returns, the interpreter raises StopIteration
# taxi.send(_.time + 10)
# # Traceback (most recent call last):
# #   File "<stdin>", line 1, in <module>
# # StopIteration
