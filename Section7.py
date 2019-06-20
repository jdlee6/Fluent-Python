'''
Function decorators and closures

function decorators let us "mark" functions in the source code to enhance their behavior 
-powerful, mastering it requires the knowledge of closures

closures are essential for effective asynchronous programming with callbacks 

decorator is a callable that takes another function as argument (decorated function)
-may perform some processing with the decorated function, returns or replaces it with another function or callable object

decorators are syntactic sugar
-can call a decorator like any regular callable, passing another function

crucial facts:
1. have the power to replace the decorated function with a different one
2. they are executed immediately when a module is loaded
'''
# example - both of the examples below have the same effect

# @decorate
# def target():
#     print('running target()')

# # or

# def target():
#     print('running target()')
# target = decorate(target)

# end result is the same: the target name refers to whatever function is returned by decorate(target)

# example - a decorator usually replaces a function with a different one

# def deco(func):
#     def inner():
#         print('running inner()')
#     # deco returns its inner function object
#     return inner

# @deco
# # target is decorated by deco
# def target():
#     print('running target()')

# # invoking the decorated target actually runs inner
# target()
# # running inner()

# # inspection reveals that target is a reference to inner
# print(target)
# # <function deco.<locals>.inner at 0x7f201a172ae8>

#########################################################################################

'''
When Python executes decorators

decorators run right after the decorated function is defined (usually at import < > or when a module is loaded by Python)
'''

# example: take a look at registration.py

'''
Note that register runs twice before any other function in the module

function decorators are executed as soon as the module is imported but the decorated functions only run when they are explicitly invoked

1. a real decorator is usually defined in one module and applied to functions in other modules
2. most decorators define an inner function and return it
'''
# import registration
# # running register<function f1 at 0x7f2b7a706ae8>
# # running register<function f2 at 0x7f2b7a706ea0>

# print(registration.registry)
# # [<function f1 at 0x7fd38819cae8>, <function f2 at 0x7fd38819cea0>]

#########################################################################################


# Decorator-enhanced Strategy pattern

'''
Recall the example from Section6 - the main issue was the repetition of function names in their definitions and 
then in the promos list used by the best_promo function to determine the highest discount applicable

problematic:
1. someone may add a new promotional strategy function and forget to manually add it to the promos list
'''
# Solution example - promos list is filled by the promotion decorator

# # promos list starts empty
# promos = []

# # promotion decorator returns promo_func unchanged, after adding it to the promos list
# def promotion(promo_func):
#     promos.append(promo_func)
#     return promo_func

# # any function decorated by @promotion will be added to promos
# @promotion
# def fidelity(order):
#     ''' 5% discount for customers with 1000 or more fidelity points '''
#     return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# @promotion
# def bulk_item(order):
#     ''' 10% discount for each LineItem with 20 or more units '''
#     discount = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount += item.total() * .1
#     return discount

# @promotion
# def large_order(order):
#     ''' 7% discount for orders with 10 or more distinct items '''
#     distinct_items = {item.product for item in order.cart}
#     if len(distinct_items) >= 10:
#         return order.total() * .07
#     return 0

# # no changes needed to best_promos, as it relies on the promos list
# def best_promo(order):
#     ''' Select best discount available '''
#     return max(promo(order) for promo in promos)

'''
This solution has several advantages over the ones presented in Section6:
1. promotion strategy functions don't have to use special names (like the _promo suffix)
2. @promotion decorator highlights the purpose of decorated function and makes it easy to temporarily disable a promotion: just comment out the decorator
3. Promotional discount strategies may be defined in other modules, anywhere in the system, as long as the @promotion decorator is applied to them

*most decorators change the decorated function - usually do it by defining an inner function and returning it to the decorated function
    -code that uses inner functions ALMOST ALWAYS depend on closures to operate coorrectly

*to understand closures, we will have to take a step back to understand how variable scopes work in Python
'''


#########################################################################################

'''
Variable Scope Rules

'''
# example - define and test a function which reads two variables: local variable a, defined as function parameter 
# and variable b that is not defined anywhere in the function

# def f1(a):
#     print(a)
#     print(b)
# f1(3)
# # NameError: name 'b' is not defined

# b = 6
# def f1(a):
#     print(a)
#     print(b)
# f1(3)
# # 3
# # 6

'''
when Python compiles the body of the function, it decides that b is a local variable because it is assigned within the function

when the call f2(3) is made, the body of f2 fetches and prints the value of the local variable a, but when trying to fetch
the value of local variable b it discovers that b is unbound
'''

# example - variable b is local because it is assigned a value in the body of the function

# b = 6
# def f2(a):
#     print(a)
#     print(b)
#     b = 9
# f2(3)
# # UnboundLocalError: local variable 'b' referenced before assignment

'''
if we want the interpreter to treat b as a global variable, we use the global declaration
'''
# b = 6
# def f3(a):
#     global b
#     print(a)
#     print(b)
#     b = 9

# f3(3)
# # 3
# # 6

# print(b)
# # 9

# b = 8
# def f3(a):
#     global b
#     print(a)
#     print(b)
#     b = 30

# f3(3)
# # 3
# # 8

# print(b)
# # 30

#########################################################################################


'''
Closures

A closure is a function with an extended scope that encompasses non-global variables referenced in the body of the function but not defined there

does NOT matter whether the function is anonymous or not; what matters is that it can access non-global variables that
are defined outside of its body
'''

# example - average_oo.py: A class to calculate a running average (class based implementation)

# example - average.py - functional implementation using a higher order function (make_averager) to calculate a running average

'''
in both examples: we call Averager() or make_averager() to get a callable object avg that will update the historical series and calculate the current mean

1st example: avg is an instance of Averager
2nd example: inner function, averager

the avg of the Averager class keeps the history in the self.series instance attribute but what about in the function?

function example:
1. series is a local variable of make_averager 
*note: when avg(10) is called, make_averager has already returned therefore the local scope is gone
2. within averager, series is a free variable (technical term meaning that the variable is NOT bound in the local scope)

inspecting the returned averager object shows how Python keeps the names of local and free variables in the __code__ attribute that represents the compiled body of the function:
(look at the inspection example below)
'''

# example - inspecting the function created by make_averager in average.py

# from average import make_averager
# avg = make_averager()
# avg(10)
# avg(11)
# avg(12)

# print(avg.__code__.co_varnames)
# # ('new_value', 'total')
# print(avg.__code__.co_freevars)
# # ('series',)

'''
binding for series is kept in the __closure__ attribute of the returned function avg.
each item in avg.__closure__ corresponds to a name in avg.__code__.co_freevars
    these items are cells and have an attribute cell_contents where the actual values can be found
'''

# print(avg.__code__.co_freevars)
# # ('series',)
# print(avg.__closure__)
# # (<cell at 0x7f1ea87e79a8: list object at 0x7f1ea88b8c88>,)
# print(avg.__closure__[0].cell_contents)
# # [10, 11, 12]

'''
to summarize:
a closure is a function that retains the bindings of the free variables that exist when the function is defined so they can be used later when the function is invoked and the defining scope is NO longer available

*the ONLY situation in which a function may need to deal with external variables that are non-global is when it is 
nested in another function
'''

#########################################################################################


'''
nonlocal declaration

a better alternative to the examples above would be to store the total and the number of items so far and compute
the mean from these two numbers
'''

# example - BROKEN higher order function to calculate a running average without keeping all history (to make a point)
# def make_averager():
#     count = 0
#     total = 0
    
#     def averager(new_value):
            # count does NOT have a value yet because we are immediately attempting +=
#         count += 1
#         total += new_value
#         return total/count

    # return averager

# avg =make_averager()
# avg(10)
# UnboundLocalError: local variable 'count' referenced before assignment

'''
-we are assigning count in the body of averager which makes it a local variable which also affects the total variable
-if you try to rebind immutable types, you are implicitly creating a local variable which is NOT a free variable therefore 
it is not saved in the closure

if a new value is assigned to a nonlocal variable - the binding stored in the closure is changed
'''

# example - Calculate a running average without keeping all history. Fixed with the use of non local

# def make_averager():
#     count = 0
#     total = 0

#     def averager(new_value):
#         nonlocal count, total
#         count += 1
#         total += new_value
#         return total / count

# return averager

#########################################################################################


'''
Implementing a simple decorator

example below is decorator that clocks every invocation of the decorated function and prints the elapsed time, the arguments passed and the result of the call 

'''

# example - a simple decorator to output the running time of functions

# import time

# def clock(func):
#     # define inner function clocked to accept ANY number of positional arguments
#     def clocked(*args):
#         t0 = time.perf_counter()
#         # this line ONLY works because the closure for clocked encompasses the func free variable
#         result = func(*args)
#         elapsed = time.perf_counter() - t0
#         name = func.__name__
#         arg_str = ', '.join(repr(arg) for arg in args)
#         # %r is the __repr__ representation for the object
#         # %0.8fs -> 8 digit float with the 's' character at the end to determine the variable as seconds
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#     # return the inner function to replace the decorated function    
#     return clocked

# # example continued - simple decorator to output the running time of  functions

# @clock
# def snooze(seconds):
#     time.sleep(seconds)

# @clock
# def factorial(n):
#     return 1 if n < 2 else n*factorial(n-1)

# if __name__=="__main__":
#     print('*' * 40, 'Calling snooze(.123)')
#     snooze(.123)
#     print('*' * 40, 'Calling factorial(6)')
#     print('6! =', factorial(6))

# # **************************************** Calling snooze(.123)
# # [0.12323493s] snooze(0.123) -> None
# # **************************************** Calling factorial(6)
# # [0.00000135s] factorial(1) -> 1
# # [0.00003281s] factorial(2) -> 2
# # [0.00006489s] factorial(3) -> 6
# # [0.00009317s] factorial(4) -> 24
# # [0.00011970s] factorial(5) -> 120
# # [0.00015171s] factorial(6) -> 720
# # 6! = 720

'''
How it works: clock gets the factorial function as its func argument, it then creates and returns the clocked function, which the Python interpreter assigns to factorial behind the scenes
'''

# # remember that this code:
# @clock 
# def factorial(n):
#     return 1 if n < 2 else n*factorial(n-1)

# # does this:
# def factorial(n):
#     return 1 if n < 2 else n*factorial(n-1)

# factorial = clock(factorial)

# factorial now holds a reference to the clocked function so each time factorial(n) is called --> clocked(n) gets executed
# print(factorial.__name__)
# # clocked

'''
in essence, clocked does:
1. records the initial time t0
2. calls the original factorial, saving the result
3. computes the elapsed time
4. formats and prints the collected data
5. returns the result saved in step 2

typical behavior of a decorator: replaces the decorated function with a new function that accepts the same arguments and returns whatever the decorated function was supposed to return, while also doing some extra processing

**Shortcomings:
    1. does NOT support keyword arguments 
    2. masks the __name__ and __doc__ of the decorated function

example below uses the functools.wraps decorator to copy the relevant attributes from func to clocked and keyword arguments are correctly handled
'''

# example - improved clock decorator

# import time, functools

# def clock(func):
#     @functools.wraps(func)
#     def clocked(*args, **kwargs):
#         t0 = time.perf_counter()
#         result = func(*args, **kwargs)
#         elapsed = time.time() - t0
#         name = func.__name__
#         arg_lst = []
#         if args:
#             arg_lst.append(', '.join(repr(arg) for arg in args))
#         if kwargs:
#             pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
#             arg_lst.append(', '.join(arg_lst))
#         arg_str = ', '.join(arg_lst)
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#     return clocked

'''
functools.wraps is one of the ready to use decorators in the standard library but theres more
'''

#########################################################################################

'''
Decorators in the standard library

Python has three built-in functions that are designed to decorate methods:
1. property
2. classmethod
3. staticmethod

Another frequently seen decorator:
1. functools.wraps - helper for building well behaved decorators

Two of the most interesting decorators in the standard library are lru_cache and singledispatch (both are in the functools module)


Memoization with functools.lru_cache
- implements memoization: an optimization technique which works by saving the results of previous invocations of an expensive function, avoiding repeat computations on previously used arguments
'''

# example - the very costly recursive way to compute the Nth number in the Fibonacci series
# @clock
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)

# if __name__=='__main__':
#     print(fibonacci(6))

# # [0.00000040s] fibonacci(0) -> 0
# # [0.00000039s] fibonacci(1) -> 1
# # [0.00003173s] fibonacci(2) -> 1
# # [0.00000020s] fibonacci(1) -> 1
# # [0.00000023s] fibonacci(0) -> 0
# # [0.00000027s] fibonacci(1) -> 1
# # [0.00002255s] fibonacci(2) -> 1
# # [0.00003399s] fibonacci(3) -> 2
# # [0.00007617s] fibonacci(4) -> 3
# # [0.00000021s] fibonacci(1) -> 1
# # [0.00000019s] fibonacci(0) -> 0
# # [0.00000023s] fibonacci(1) -> 1
# # [0.00000992s] fibonacci(2) -> 1
# # [0.00002054s] fibonacci(3) -> 2
# # [0.00000020s] fibonacci(0) -> 0
# # [0.00000023s] fibonacci(1) -> 1
# # [0.00001060s] fibonacci(2) -> 1
# # [0.00000024s] fibonacci(1) -> 1
# # [0.00000023s] fibonacci(0) -> 0
# # [0.00000026s] fibonacci(1) -> 1
# # [0.00001062s] fibonacci(2) -> 1
# # [0.00002082s] fibonacci(3) -> 2
# # [0.00004153s] fibonacci(4) -> 3
# # [0.00007189s] fibonacci(5) -> 5
# # [0.00015892s] fibonacci(6) -> 8
# # 8

''' if we add the lines to use lru_cache, performance is much improved; see the example below '''

# example - faster implementation of caching

# import functools

# # note that lru_cache MUST be invoked as a regular function (can accept configuration parameters)
# @functools.lru_cache()
# # this is an example of stacked decorators: @lru_cache() is applied on the function returned by @clock
# @clock
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)

# if __name__=="__main__":
#     print(fibonacci(6))

# # Notice how the execution time is halved and the function is called only once for each value of n
# # [0.00000039s] fibonacci(0) -> 0
# # [0.00000042s] fibonacci(1) -> 1
# # [0.00005298s] fibonacci(2) -> 1
# # [0.00000075s] fibonacci(3) -> 2
# # [0.00006601s] fibonacci(4) -> 3
# # [0.00000053s] fibonacci(5) -> 5
# # [0.00007905s] fibonacci(6) -> 8
# # 8

'''
optional arguments that can be passed into lru_cache:
1. maxsize=<int> - determines how many call results are stored - older results are discarded to make room
2. typed=<Boolean> - if set to True; stores results of different argument types separately i.e. distinguishing between float and integer arguments that are normally considered equal like 1 and 1.0

*uses a dict to store the results and keys are made from the positional and keyword arguments used in the calls; all arguments taken by the decorated function MUST be hashable


Generic functions with single dispatch
'''
# example - generate HTML displays for different types of Python objects 
# import html

# def htmlize(obj):
#     content = html.escape(repr(obj))
#     return '<pre>{}</pre>'.format(content)

'''
let's extend it so that:
str: replace embedded new line characters with '<br>\n>' and use <p> tags instead of <pre>
int: show the number in decimal and hexadecimal
lists: output an HTML list, formatting each item according to its type
'''

# example: htmlize generates HTML tailored to different object types

# # by default, the HTML-escaped repr of an object is shown enclosed in <pre></pre>
# print(htmlize({1, 2, 3}))
# # <pre>{1, 2, 3}</pre>

# print(htmlize(abs))
# # <pre>&lt;built-in function abs&gt;</pre>

# # str objects are also HTML-escaped but wrapped in <p></p> with <br> line breaks
# print(htmlize('Heimlich & Co.\n- a game'))
# # <pre>&#x27;Heimlich &amp; Co.\n- a game&#x27;</pre>

# # an int is shown in decimal and hexadecimal inside <pre></pre>
# print(htmlize(42))
# # '<pre>42 (0x2a)</pre>'

# # each list item is formatted according to its type, and the whole sequence rendered as an HTML list
# print(htmlize(['alpha', 66, {3, 2, 1}]))
# # <ul>
# # <li><p>alpha</p></li>
# # <li><pre>66 (0x42)</pre></li>
# # <li><pre>{1, 2, 3}</pre></li>
# # </ul>

'''
can't create variations of htmlize with different signatures for each data type so a solution in Python would be to turn htmlize into a dispatch function, with a chain of if/elif/elif calling specialized functions like htmlize_str, htmlize_int,etc . . .

the functools.singledispatch decorator allows each module to contribute to the overall solution and lets you easily provide a specialized function even for classes that you CAN'T edit

if you decorate a function with @singledispatch
    -becomes a generic function: a group of functions to perform the same operation in different ways, depending on the type of the first argument
'''

# example - singledispatch creates a custom htmlize.register to bundle several functions into a generic function

# from functools import singledispatch
# from collections import abc
# import numbers, html

# # @singledispatch marks the base function which handles the object type
# @singledispatch
# def htmlize(obj):
#     content = html.escape(repr(obj))
#     return f'<pre>{content}<pre>'

# # each specialized function is decorated with @<<base_function>>.register(<<type>>)
# @htmlize.register(str)
# # the name of the specialized functions is irrelevant; _ is a good choice to make this clear
# def _(text):
#     content = html.escape(text).replace('\n', '<br>\n')
#     return f'<p>{0}</p>'.format(content)

# # for each additional type to receive special treatment, register a new function. numbers.Integral is a virtual superclass of int (see below)
# @htmlize.register(numbers.Integral)
# def _(n):
#     return '<pre>{0} (0x{0:x})</pre>'.format(n)

# # You can stack several register decorators to support different types with the same function
# @htmlize.register(tuple)
# @htmlize.register(abc.MutableSequence)
# def _(seq):
#     inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
#     return '<ul>\n<li>' + inner + '</li>\n</ul>'

'''
singledispatch
1. you can register specialized functions anywhere in the system, in any module
*easily provide new custom function to handle type and write custom functions for classes that you did NOT write and CAN'T change
'''

#########################################################################################


'''
Stacked decorators
when two decorators @d1 and @d2 are applied to a function f in that order, the result is the same as f = d1(d2(f))


some decorators may also take arguments such as @lru_cache() and the htmlize.register(<<type>>) produced by @singledispatch

Parametrized Decorators

make a decorator factory that takes those specified arguments and returns a decorator, which is then applied to the function to be decorated
'''

# example - abridged registration.py module from example repeated here for convenience
# registry = []

# def register(func):
#     print('running register(%s)' % func)
#     registry.append(func)
#     return func

# @register
# def f1():
#     print('running f1()')

# print('running main()')
# print('registry ->', registry)
# f1()

# # running register(<function f1 at 0x7f1f29776ae8>)
# # running main()
# # registry -> [<function f1 at 0x7f1f29776ae8>]
# # running f1()


'''
parametrized registration decorator

optional 'active' parameter which, if False will skip registering the decorated function
new register function is NOT a decorator but a decorator factory
-when called, it returns the actual decorator that will be applied to the target function
'''

# example - accept parameters, the new register decorator must be called as a function

# # registry is now a set, so adding and removing functions is FASTER
# registry = set()

# # register takes an optional keyword argument
# def register(active=True):
#     # the decorate inner function is the actual decorator; note how it takes a function as argument
#     def decorate(func):
#         print('running register(active=%s -> decorate(%s)' % (active, func))
#         # Register func only if the active argument (retrieved from the closure) is True
#         if active:
#             registry.add(func)
#         else:
#             # if not active and func in registry, remove it
#             # discard() is a set method that removes a specified element from the set
#             registry.discard(func)
#         # because decorate is a decorator, it must return a function
#         return func
#     # register is our decorator factory, so it return decorate
#     return decorate

# # the @register factory must be invoked as a function, with the desired parameters
# @register(active=False)
# def f1():
#     print('running f1()')

# # if NO parameters are passed, register must still be called as a function - @register() - to return the actual decorator, decorate
# @register()
# def f2():
#     print('running f2()')

# def f3():
#     print('running f3()')

# # running register(active=False -> decorate(<function f1 at 0x7fd43dceeea0>)
# # running register(active=True -> decorate(<function f2 at 0x7fd43dcee9d8>)

# # f2 is in the registry because of how it was loaded from the previous invokations
# print(registry)
# # {<function f2 at 0x7f3f6f1c39d8>}

'''
register() returns decorate which is then applied to the decorated function

note how only the f2 function appears in the registry; f1 is NOT there because active=False
*instead of using the @ syntax and we used register as a regular function
-the syntax needed to decorate a function f would be register()(f) which would add f to the registry
or
-register(active=False)(f) to not add it

parametrized decorators usually replace the decorated function and their construction requires yet another level of nesting
-almost always involve at LEAST two nested functions
'''

# # register() expression returns decorate, which is then applied to f3
# print(register()(f3))
# # running register(active=True -> decorate(<function f3 at 0x7f18b491dae8>)
# # <function f3 at 0x7f18b491dae8>

# # the previous line added f3 to the registry
# print(registry)
# # {<function f2 at 0x7f18b491d9d8>, <function f3 at 0x7f18b491dae8>}

# # this call removes f2 fromthe registry
# print(register(active=False)(f2))
# # running register(active=False -> decorate(<function f2 at 0x7f18b491d9d8>)
# # <function f2 at 0x7f18b491d9d8>

# # confirms that only f3 remains in the registry
# print(registry)
# # {<function f3 at 0x7f18b491dae8>}

'''
parametrized clock decorator

revisit the clock decorator and add a feature that lets users may pass a format string to control the output of the decorated function
'''

# example - parametrized clock decorator

import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

# clock is our parametrized decorator factory
def clock(fmt=DEFAULT_FMT):
    # decorate is the actual decorator
    def decorate(func):
        # clocked wraps the decorated function
        def clocked(*_args):
            t0 = time.time()
            # _result is the actual result of the decorated function
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            # _args holds the actual arguments of clocked, while args is str used for display
            args = ', '.join(repr(arg) for arg in _args)
            # result is the str representation of _result, for display
            result = repr(_result)
            # using **locals() here allows any local variable of clocked to be referenced in the fmt
            print(fmt.format(**locals()))
            # clocked will replace the decorated function, so it should return whatever that function returns
            return result
        # decorate returns clocked    
        return clocked
    # clock returns decorate
    return decorate

if __name__ == "__main__":
    # # In this self test, clock() is called without arguments, so the decorator applied will use the default format str
    # @clock()
    # def snooze(seconds):
    #     time.sleep(seconds)

    # for i in range(3):
    #     snooze(.123)

# [0.12319779s] snooze(0.123) -> None
# [0.12318492s] snooze(0.123) -> None
# [0.12323213s] snooze(0.123) -> None


    # @clock('{name}: {elapsed}s')
    # def snooze(seconds):
    #     time.sleep(seconds)

    # for i in range(3):
    #     snooze(.123)

# snooze: 0.12315487861633301s
# snooze: 0.12322425842285156s
# snooze: 0.12323880195617676s


    # @clock('{name}({args}) dt={elapsed:0.3f}s')
    # def snooze(seconds):
    #     time.sleep(seconds)
    
    # for i in range(3):
    #     snooze(.123)

# snooze(0.123) dt=0.123s
# snooze(0.123) dt=0.123s
# snooze(0.123) dt=0.123s