'''
Functions are first class objects
1. created @ runtime
2. assigned to a variable or element in a data structure
3. passed as an argument to a function
4. returned as the result of a function

Treating a function like an object: look at the example below
'''
# create a function in "run time"
# def factorial(n):
#     '''
#     returns n
#     '''
#     # ternary conditional 
#     return 1 if n <2 else n * factorial(n-1)

# print(factorial(5))
# # 120

# # __doc__ is one of several attributes of function objects
# # used to generate the help text of an object
# print(factorial.__doc__)

#     # returns n

# # factorial is an instance of the function class    
# print(type(factorial))
# # <class 'function'>

# # We can assign the function above a variable and call it through that name
# # We can also pass factorial as an argument to map 
# # map function returns an iterable where each item is the result of the application of the first argument (function) to successive elements of the second argument (iterable)

# fact = factorial
# print(fact)
# # <function factorial at 0x7f08c085f1e0>

# print(fact(5))
# # 120

# print(map(factorial, range(11)))
# # <map object at 0x7f4513133780>

# print(list(map(fact, range(11))))
# # [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

###############################################################################


'''
Higher-order functions

function that takes a function as an argument or returns a function as result is a higher-order function
ie. map(), sorted() - optional keyword - sort - is a function
'''
# # Sorting a list of words by length
# fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# # function here is the len argument
# print(sorted(fruits, key=len))
# # ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']

# # Sorting a list of words by their reversed spelling
# def reverse(word):
#     return word[::-1]
# print(reverse('testing'))
# # gnitset
# print(sorted(fruits, key=reverse))
# # ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

###############################################################################


'''
Modern replacements for map, filter, reduce

map and filter functions are built in functions - returns generators (a form of an iterator)
listcomp / genexp does the job of both and is MORE readable
'''
# # build a list of factorials from 0! to 5!
# print(list(map(fact, range(6))))
# # [1, 1, 2, 6, 24, 120]

# # same operation with a list comprehension
# print([
#     fact(n) for n in range(6)
# ])
# # [1, 1, 2, 6, 24, 120]

# # list of factorials of odd numbers upto 5! using both map and filter
# print(list(map(factorial, filter(lambda n: n%2, range(6)))))
# # [1, 6, 120]

# # list comprehensions do the same job (replaces map and filter which make lambda unnecessary)
# print([
#     factorial(n) for n in range(6) if n % 2
# ])
# # [1, 6, 120]

'''
Example - sum of integers up to 99 performed with reduce and sum

all(iterable) - True if every element of iterable is truthy
any(iterable) - True if any element of iterable is truthy

to use a higher order function, sometimes it is convenient to create a small, one off function
'''


# # reduce is not a built in function anymore (after Python3)
# from functools import reduce
# # import add to avoid creating a function just to add two numbers
# from operator import add

# # sum integers up to 99
# print(reduce(add, range(100)))
# # 4950

# # same task; import or adding function NOT needed
# print(sum(range(100)))
# # 4950


###############################################################################


''' 
Anonymous functions

lambda keyword creates an anonymous function within a Python expression
- body of a lambda CANNOT make assignments or use any other Python statement (while, try, etc...)
    
if hard to read:
    1. write a comment explaining what that lambda does
    2. study the comment
    3. convert to a def statement 
    4. remove comment
'''

# # example - sorting a list of words by their reversed spelling using lambda
# fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# # lambda is taking the single argument word and then returning word[::-1]
# print(sorted(fruits, key=lambda word: word[::-1]))
# # ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

###############################################################################


'''
Seven flavors of callable objects
- to determine whether an object is callable (use callable())

user-defined functions - def statements or lambda
built-in functions - len or time.strftime
built-in methods - dict.get
methods - functions defined in a class
Class - calling a class is like calling a function
Class Instances - if class has __call__ then callable
Generator functions - functions or methods that use the yield keyword (generator functions return a generator object)
'''

# User defined functions

# example - BingoCage - purpose is to pick items from a shuffled list

# import random

# class BingoCage:
#     def __init__(self, items):
#         # single underscore: intended to be used internally
#         # __init__ accepts any iterable; building a local copy prevents unexpected side effects on any list pass as an argument
#         self._items = list(items)
#         #shuffle is guaranteed to work because self._items is a list
#         random.shuffle(self._items)

#     # the main method
#     def pick(self):
#         try:
#             return self._items.pop()
#         except IndexError:
#             # Raise exception with custom message if self._items if empty
#             raise LookupError('pick from empty Bingo Cage')

#     # Shortcut to bingo.pick(): bingo()
#     # makes it a callable object see the example below
#     def __call__(self):
#         return self.pick()


# bingo = BingoCage(range(3))
# print(bingo.pick())
# # 0
# print(bingo())
# # 1
# print(callable(bingo))
# # True


###############################################################################


''' 
Function introspection

__doc__ 
dir()
__dict__ - stores user attributes assigned to a user-defined class
. . .
'''

# Example - Listing attributes of functions that don't exist in plain instances

# create bare user-defined class
# bare-est is absolutely nothing but pass in the class/function
# class C: pass

# # make an instance of class C stored in obj
# obj = C()

# # create a bare function
# def func(): pass

# # using set difference, generate a sorted list of the attributes that exist in a function but NOT in an instance of a bareclass
# print(sorted(set(dir(func)) - set(dir(obj))))
# # ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']


###############################################################################


'''
From positional to keyword only parameters

* and **

* unpacks positional arguments
** unpacks keyword arguments (dict)

cls - means that method belongs to class
self - means that method is related to an instance of the class
'''

# Example - tag generates HTML

def tag(name, *content, cls=None, **attrs):
    ''' 
    Generate one or more HTML tags
    '''
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ' '.join('%s=%s' % (attr, value)
                        for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

# # single positional argument produces an empty tag with that name
# print(tag('br'))
# # <br/>

# # any number of arguments after the first are captured by *content as a tuple
# print(tag('p', 'hello'))
# # <p>hello</p>
# print(tag('p', 'hello', 'world'))
# # <p>hello</p>
# # <p>world</p>

# # Keyword arguments not explicitly named in the tag signature are captured by **attrs as a dict
# print(tag('p', 'hello', id=33))
# # <p id=33>hello</p>

# # The cls parameter can only be passed as a keyword argument
# print(tag('p', 'hello', 'world', cls='sidebar'))
# # <p class=sidebar>hello</p>
# # <p class=sidebar>world</p>

# # Even the first positional argument can be passed as a keyword when tag is called
# print(tag(content='testing', name="img"))
# # <img content=testing />

# # Prefixing the my_tag dict with ** passes all its items as separate arguments which are then
# # bound to the named parameters, with the remaining caught by **attrs
# my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
# print(tag(**my_tag))
# # <imgclass=framed src=sunset.jpg title=Sunset Boulevard />


# if you dont want to support variable positional arguments but still want keyword-only arguments, put a * by itself in the signature
# parameters after * are keyword only parameters and may only be passed as kwargs
# keyword-only arguments do NOT need to have a default value: they can be MANDATORY like b
# def f(a, *, b):
#     return a, b

# print(f(1, b=2))
# # (1, 2)

# print(f(1, 2))
# # TypeError: f() takes 1 positional argument but 2 were given



###############################################################################


'''
Retrieving information about parameters

Bobo http micro-framework
'''

# example - Bobo knows that hello requires a person argument, and retrieves from the HTTP request
# to run bobo -> bobo -f Section5.py -> http://localhost:8080/

# import bobo

# @bobo.query('/')
# # retrieves a parameter with that name from the request and pass it to hello
# def hello(person):
#     return f'Hello {person}!'

# # when we run this - it will generate a 403 error because the person was not found in the request
# # solution: http://localhost:8080/?person=Bob --> will generate a 200 http message because the person parameter was found

'''
__default__ attr. holds a tuple with default values of positional and keyword args
__kwdefaults__ attr. displays the defaults for keyword-only arguments
__code__ attr. is where the names of the arguments are found 
'''

# example - function to shorten a string by clipping at a space near the desired length

# def clip(text, max_len=80):
#     ''' Return text clipped at the last space before or after max_len '''
#     end = None
#     if len(text) > max_len:
#         # string to be searched, starting index of string, ending index of string
#         space_before = text.rfind(' ', 0, max_len)
#         if space_before > 0:
#             end = space_before
#         else:
#             space_after = text.rfind(' ', max_len)
#             if space_after >= 0:
#                 end = space_after
#     # no spaces were found
#     if end is None: 
#         end = len(text)
#     return text[:end].rstrip()


# # Extracting information about the function arguments
# print(clip.__defaults__)
# # (80,)
# print(clip.__code__)
# # <code object clip at 0x7fc31e0b36f0, file "Section5.py", line 336>

# # note how not ONLY the argument names are printed but also the local variables in the body of the function
# print(clip.__code__.co_varnames)
# # ('text', 'max_len', 'end', 'space_before', 'space_after')

# # does not include any variable arguments prefixed with * and **
# print(clip.__code__.co_argcount)
# # 2


# The __code__. < > is awkward, the example below is much better and more readable (uses the inspect module)

# from inspect import signature

# sig = signature(clip)
# print(sig)
# # (text, max_len=80)

# print(str(sig))
# # (text, max_len=80)

# # each parameter instance has attributes such as name, default and kind
# for name, param in sig.parameters.items():
#     print(param.kind, ':', name, '=', param.default)
# # POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
# # POSITIONAL_OR_KEYWORD : max_len = 80

'''
kind attribute holds 1 of 5 possible values from _ParameterKind class:
1. POSITIONAL_OR_KEYWORD - parameter that may be passed as positional or as kwarg
2. VAR_POSITIONAL - tuple of positional parameteres
3. VAR_KEYWORD - a dict of keyword parameters
4. KEYWORD_ONLY - a keyword only parameter
5. POSITONAL_ONLY - positional only parameter

inspect.Parameter objects have an annotiation attribute which is usually inspect.empty 
inspect.Signature object has a bind method that takes any number of arguments and binds them to the parameters in the signature
'''

# # example - binding the function signature from the tag function 
# import inspect

# # get the signature from tag function
# sig = inspect.signature(tag)
# my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}

# # pass a dict of arguments to .bind()
# bound_args = sig.bind(**my_tag)
# # an inspect.BoundArguments object is produced
# print(bound_args)
# # <BoundArguments (name='img', cls='framed', attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>

# # iterate over the items in bound_args.arguments, which is an OrderedDict, to display names and values of the arguments
# for name, value in bound_args.arguments.items():
#     print(name, '=', value)
# # name = img
# # cls = framed
# # attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}

# # Remove the mandatory argument from my_tag
# del my_tag['name']

# # Calling sig.bind(**my_tag) raises a TypeError complaining of the missing name parameter
# bound_args = sig.bind(**my_tag)
# # TypeError: missing a required argument: 'name'


###############################################################################


'''
Function annotations

annotation expression preceded by :.
if default value - annotation goes between the argument name and the = sign
to annotate the return value, add -> and another expression between the ) and the : @ the tail of the function declaration

most common types in annotations are classes (str or int, or strings like 'int > 0')
no processing is done with annotiations and are merely stored in __annotations__ attribute of the function, a dict:
'''

# annotated function declaration
# def clip(text:str, max_len:'int >0'=80) -> str:
#     ''' return text clipped at the last space before or after max_len '''
#     end = None
#     if len(text) > max_len:
#         # string to be searched, starting index of string, ending index of string
#         space_before = text.rfind(' ', 0, max_len)
#         if space_before > 0:
#             end = space_before
#         else:
#             space_after = text.rfind(' ', max_len)
#             if space_after >= 0:
#                 end = space_after
#     # no spaces were found
#     if end is None: 
#         end = len(text)
#     return text[:end].rstrip()

# print(clip.__annotations__)
# # {'text': <class 'str'>, 'max_len': 'int >0', 'return': <class 'str'>}


# from inspect import signature

# sig = signature(clip)
# # signature function returns a Signature object which has a return_annotation attribute and a parameters dictionary mapping parameter names to Parameter objects
# print(sig.return_annotation)
# # <class 'str'>
# for param in sig.parameters.values():
#     note = repr(param.annotation).ljust(13)
#     print(note, ':', param.name, '=', param.default)
# # <class 'str'> : text = <class 'inspect._empty'>
# # 'int >0'      : max_len = 80


###############################################################################


'''
Packages for functional programming

modules:
operator 
functool 
'''

# example - factorial implemented with reduce and an anonymous function

# from functools import reduce

# # reduce(function, iterable[, initializer])
# # when initial value is provided, the function is called with the initial value and the first item from the sequence
# def fact(n):
#     return reduce(lambda a, b: a*b, range(1, n+1))
#     # starts @ 1
#     # (((1*2)*3)*4)*5) . . .

# the operator module provides function equivalents for dozens of arithmetic operators

# example - factorial implemented with reduce and operator.mul (helps avoid lambda)

# from functools import reduce
# from operator import mul

# def fact(n):
#     return reduce(mul, range(1, n+1))

'''
Another group of one trick lambdas that operator REPLACES: itemgetter / attrgetter

itemgetter: sorting a list of tuples by value of one field; if multiple values then returns fields with those index #s (uses the [] operator)
attrgetter: creates functions to extract object attributes by name; if multiple names as arguments then returns a tuple of values
    i. if any argument name contains a .(dot), attrgetter navigates through nested objects to retrieve the attribute

methodcaller: somewhat similar to itemgetter and attrgetter in that it creates a function on the fly (function it creates calls a method by name on the object given as argument)
'''

# cities are printed sorted by country code (field 1) - itemgetter(1) does the same as lambda fields: fields[1]
metro_data =[
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi  NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
]

# from operator import itemgetter

# for city in sorted(metro_data, key=itemgetter(1)):
#     print(city)
# # ('Delhi  NCR', 'IN', 21.935, (28.613889, 77.208889))
# # ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# # ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
# # ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))

# if you pass multiple index arguments to itemgetter, the function it builds will return tuples with the extracted values
# cc_name = itemgetter(1, 0)
# for city in metro_data:
#     print(cc_name(city))

# # ('JP', 'Tokyo')
# # ('IN', 'Delhi  NCR')
# # ('MX', 'Mexico City')
# # ('US', 'New York-Newark')


# Example - demo of attrgetter to process a previously defined list of namedtuple called metro_data
# from collections import namedtuple

# # use namedtuple to define LatLong
# LatLong = namedtuple('LatLong', 'lat long')

# # also define Metropolis
# Metropolis = namedtuple('Metropolis', 'name cc pop coord')

# # build metro_areas list with Metropolis instances; note the nested tuple unpacking to extract (lat, long) and use them to build the LatLong for the coord attribute of Metropolis
# metro_areas = [
#     Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data
# ]
# print(metro_areas[0])
# # Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))

# # Reach into element metro_areas[0] to get its latitude
# print(metro_areas[0].coord.lat)
# # 35.689722

# from operator import attrgetter

# # define an attrgetter to retrieve the name and the coord.lat nested attribute
# name_lat = attrgetter('name', 'coord.lat')

# # use attrgetter again to sort list of cities by latitude
# for city in sorted(metro_areas, key=attrgetter('coord.lat')):
#     # use the attrgetter defined in named_lat to show only city name and latitude
#     print(name_lat(city))
# # ('Mexico City', 19.433333)
# # ('Delhi  NCR', 28.613889)
# # ('Tokyo', 35.689722)
# # ('New York-Newark', 40.808611)

# list of functions defined in operator (excluding the ones that start with '_')
# import operator
# print([
#     name for name in dir(operator) if not name.startswith('_')
# ])
# # ['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']
# # operators that start with an i - correspond to the augmented assignment operators (change first argument in place if mutable; if not the function works like the one without the i prefix and simply returns the result of the operation)


# example - demo of methodcaller

# from operator import methodcaller

# s = 'The time has come'
# upcase = methodcaller('upper')
# print(upcase(s))
# # THE TIME HAS COME

# # or

# # if you need to use the str.upper as a function you can just call it on the str class and pass a string as argument
# print(str.upper(s))
# # THE TIME HAS COME

# # replace is the function, ' ' is what we want to replace with '-'
# hiphenate = methodcaller('replace', ' ', '-')
# print(hiphenate(s))
# # The-time-has-come


###############################################################################


'''
Freezing arguments with functools.partial

.partial - higher order function that allows partial application of a function --> produces a new callable with some of the arguments of the original function fixed 
.partialmethod - does the same job as .partial but is designed to work with methods
'''

# example - using partial to use a 2 argument function where a 1 argument callable is required

from operator import mul
from functools import partial

# create new triple function from mul, binding first positional to 3
triple = partial(mul, 3)

# test it
print(triple(7))
# 21

# use triple with map; mul would not work with map in this example
print(list(map(triple, range(1, 10))))
# [3, 6, 9, 12, 15, 18, 21, 24, 27]


# example - building a convenient Unicode normalizing function with partial
# import unicodedata, functools

# # partial takes a callable as first argument, followed by an arbitray number of positional and keyword arguments to bind
# nfc = functools.partial(unicodedata.normalize, 'NFC')
# s1 = 'café'
# s2 = 'cafe\u0301'
# print(s1, s2)
# # café café

# print(s1 == s2)
# # False

# print(nfc(s1) == nfc(s2))
# # True


# example - shows the use of partial with the tag function from the def statement above to FREEZE one positional argument and one keyword argument

# import tag from the previous example and show its id
print(tag)
# <function tag at 0x7f6bc2a8d1e0>

from functools import partial

# create picture function from tag by fixing the first positional argument with 'img' and the cls keyword argument with 'pic-frame'
picture = partial(tag, 'img', cls='pic-frame')

# picture works as expected
print(picture(src='wumpus.jpeg'))
# <img class="pic-frame" src="wumpus.jpeg"/>

# partial() returns a functools.partial object
print(picture)
# functools.partial(<function tag at 0x7fbedb10c1e0>, 'img', cls='pic-frame')

# a functools.partial object has attributes providing access to the original function and the fixed arguments
print(picture.func)
# <function tag at 0x7f96dcc531e0>

print(picture.args)
# ('img',)

print(picture.keywords)
# {'cls': 'pic-frame'}