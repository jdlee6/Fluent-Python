'''
Sequence hacking, hashing and slicing 


Vector: a user-defined type
    -strategy to implement Vector will be to use composition and NOT inheritance


Vector take #1: Vector2d compatible (Not compatible with Vector2d based on design)
    -best practice for a sequence constructor is to take data as an iterable argument in the constructor like all built-in sequence types do
'''

# example - Tests of Vector.__init__ and Vector.__repr__ (take a look at vector_v1.py for the class object Vector)

# from Sec10_examples.vector_v1 import Vector

# print(repr(Vector([3.1, 4.2])))
# # Vector([3.1, 4.2])

# print(repr(Vector((3, 4, 5))))
# # Vector([3.0, 4.0, 5.0])

# # when a Vector has more than 6 components, the string produced by repr() is abbreivated with ...
# # repr is used for debugging - you don't want a single large object to span thousands of lines
# # the reprlib module is used to produce limited length representations
# print(repr(Vector(range(10))))
# # Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])

'''
reprlib.repr() is a function that produces safe representations of large or recursive structures by LIMITING the length of the output string and marking the cut with '...'
    ie. we used it to make 'Vector(array('d', [3.0, 4.0, 5.0]))' look like 'Vector([3.0, 4.0, 5.0])'


Protocols and duck typing

protocol is an informal interface defined in documentation and not in code
sequence protocol entails the __len__ and __getitem__ methods

the example below implements the sequence protocol even if that is NOT declared anywhere in the code
    -we say it IS a sequence because it BEHAVES like one which is also known as duck typing

*often can get away implementing PART of a protocol
    ie. to support iteration __getitem__ is required where as __len__ is not
'''
# example 

# import collections

# Card = collections.namedtuple('Card', ['rank', 'suit'])

# class FrenchDeck:
#     ranks = [str(n) for n in range(2, 11) + list('JQKA')]
#     suits = 'spades diamonds clubs hearts'.split()

#     def __init__(self):
#         self._cards = [Card(rank, suit) for suit in self.suits
#                                                          for rank in self.ranks]

#     def __len__(self):
#         return len(self._cards)

#     def __getitem__(self, position):
#         return self._cards[position]


'''
Vector take #2: a sliceable sequence

the __len__ and __getitem__ methods are a good start
'''

# add the following to vector_v1.py

# class Vector:
#     # . . .
#     # lines omitted

#     def __len__(self):
#         return len(self._components)

#     def __getitem__(self, index):
#         return self._components[index]

# example

# from Sec10_examples.vector_v1 import Vector

# v1 = Vector([3, 4, 5])
# print(len(v1))
# # 3

# print((v1[0], v1[-1]))
# # (3.0, 5.0)

# v7 = Vector(range(7))
# # slicing is supported but not very well; we want the slice to be a Vector instance and NOT an array
# print(v7[1:4])
# # array('d', [1.0, 2.0, 3.0])

'''
consider the built in sequence types: EVERY one of them, when sliced, produces a NEW instances of its OWN type and not of some other type

to make Vector produce slices as Vector instance - we can't just delegate slicing to array; we need to analyze the arguments we get in __getitem__


How slicing works
'''
# example - checking out the behavior of __getitem__ and slices

# class MySeq:
#     def __getitem__(self, index):
#         # for this demonstration, __getitem__ merely returns whatever is passed to it
#         return index

# s = MySeq()
# # a single index, nothing new
# print(s[1])
# # 1

# # the notation 1:4 becomes slice(1, 4, None)
# print(s[1:4])
# # slice(1, 4, None)

# # slice(1, 4, 2) means start at 1, stop at 4, step by 2
# print(s[1:4:2])
# # slice(1, 4, 2)

# # The presence of commas INSIDE the [] means __getitem__ receives a tuple
# print(s[1:4:2, 9])
# # (slice(1, 4, 2), 9)

# # the tuple may even hold several slice objects
# print(s[1:4:2, 7:9])
# # (slice(1, 4, 2), slice(7, 9, None))


# # example - checking out the behavior of __getitem__ and slices

# # slice is a built-in type
# print(slice)
# # <class 'slice'>

# # inspecting a slice we find the data attributes start, stop and step and an indices method
# print(dir(slice))
# # ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']

'''
print(help(slice.indices))
    indices attributes
        indices(...)
        S.indices(len) -> (start, stop, stride)
        
        Assuming a sequence of length len, calculate the start and stop
        indices, and the stride length of the extended slice described by
        S. Out of bounds indices are clipped in a manner consistent with the
        handling of normal slices.
'''

# example - considering a sequence of len == 5; 'ABCDE'

# # changes the length of the len(slice) to 6
# # can not be negative because the length should NOT be negative
# print(slice(None, 10, 2).indices(6))
# # (0, 6, 2)

# # if the argument passed in indices is bigger than the length, it will just return the maximum slice of the length
# print(slice(None, 10, 2).indices(20))
# # (0, 10, 2)

# # 'ABCDE'[:10:2] is the same as 'ABCDE'[0:5:2]
# print(slice(None, 10, 2).indices(5))
# # (0, 5, 2)

# #'ABCDE'[-3:] is the same as 'ABCDE'[2:5:1]
# print(slice(-3, None, None).indices(5))
# # (2, 5, 1)


'''
a slice-aware __getitem__

the example below lists two methods needed to make Vector behave as a sequence: __len__ and __getitem__ 
'''

# example - look at vector_v2.py: __len__ and __getitem__ methods have been added to Vector class from vector_v1.py

# example - Tests of enhanced Vector.__getitem__ from Example 10-6

# from Sec10_examples.vector_v2 import Vector

# v7 = Vector(range(7))

# # an intenger index retrieves jsut one component value as a float
# print(v7[-1])
# # 6.0

# # a slice index creates a new Vector
# print(v7[1:4])
# # (1.0, 2.0, 3.0)

# # A slice of len == 1 also creates a Vector
# print(v7[-1:])
# # (6.0,)

# # Vector does not support multi-dimensional indexing, so a tuple of indices or slices raises an error
# print(v7[1, 2])
# # TypeError: Vector indices must be integers


'''
Vector take #3: Dynamic Attribute Access

__getattr__ is a special method that provides a better way of accessing components instead of using the @property decorator (we use __getattr__ because it is too tedious to write multiple property decorators in Vector)

__getattr__ method is invoked by the interpreter when the attribute lookup FAILS

myobj.x --> it would check myobj instance for an attribute named x; if not the search goes to the class (myobj.__class__) and looks through the inheritance graph

if the x attribute is still not found; the __getattr__ method defined in the class of my_obj is called with self and the name of the attribtues as a string
'''

# problem - while adjusting from Vector2d to Vector; we lost the ability to access our components with v.x, v.y as we have multiple variables

# instead of having the Vector object return: 
# AttributeError: 'Vector' object has no attribute 'x'

# # this is what we want the Vector object to return
# from Sec10_examples.vector_v2 import Vector

# v = Vector(range(10))
# print(v.x)
# # 0.0
# print(v.y, v.z, v.t)
# # (1.0, 2.0, 3.0)


# Look at vector_v3.py: __getattr__ method added to Vector class; BUT it's not enough 
# example - Inappropriate behavior: assigning to v.x raises no error but introduces an inconsistency

# from Sec10_examples.vector_v3 import Vector

# v = Vector(range(5))
# print(repr(v))
# # Vector([0.0, 1.0, 2.0, 3.0, 4.0])

# # Access element v[0] as v.x
# print(v.x)
# # 0.0

# # Assign new value to v.x. This should raise an exception
# v.x = 10

# # Reading v.x shows the new value
# print(v.x)
# # 10

# # The vector components did not change
# print(repr(v))
# # Vector([0.0, 1.0, 2.0, 3.0, 4.0])

'''
Notice how the Vector array object does NOT have v.x assigned to 10.

Python only calls the __getattr__ method as a fall back when the object does NOT have the named attribute but because we assign v.x = 10 the v object now has an x attribute so __getattr__ will no longer be called to retrieve v.x: the interpreter will just return the value 10 that is bound to v.x

need to customize the logic for setting attributes in our Vector class in order to avoid inconsistency 

note: very often when you implement __getattr__; you need to code __setattr__ as well to avoid inconsistent behavior in your objects
'''

# Look at vector_v3.py: __setattr__ method in Vector class has been added

'''
Vector take #4: hashing and a faster == 

We want to apply the ^ (xor) operator to the hashes of every component, in succession like this: v[0] ^ v[1] ^ v[2] (functools.reduce() - computing the hash of all vector components)
    *reducing functions - reduce, sum, any, all - produce a single aggregate result from a sequence or from any finite iterable object

    -reduce a series of values to a single value
    -1st argument in reduce() is a 2-argument function and the second argument is an iterable
    -reduce(fn, lst) fn will be applied to the first pair of elements fn(lst[0], lst[1]), which produces a first result, r1
        -fn(r1, lst[2]) --> produces 2nd result, r2 --> fn (r2, lst[3]) produces 3rd result and so on...
        - this keeps going until the last element is a single result that is returned

reduce(function, iterable, initializer): good to throw in a 3rd argument so you prevent an exception: 
    TypeError: reduce() of empty sequence with no initial value
    **for +, |, ^ initializer should be 0; for *, & it should be 1
'''
# # example of reduce with 5!
# print(2 * 3 * 4 * 5)
# # 120

# import functools
# print(functools.reduce(lambda a,b: a*b, range(1,6)))
# # 120

# # How it works: 
# # 1 * 2 = 2 
# # 2 * 3 = 6
# # 6 * 4 = 24
# # 24 * 5 = 120

# example - three ways of calculating the accumulated xor of integers from 0 to 5

# Aggregrate xor with a for loop and an accumulator variable
# n = 0
# for i in range(1, 6):
#     n ^= i
# print(n)
# # 1

# # functools.reduce using an anonymous function
# import functools
# print(functools.reduce(lambda a, b: a^b, range(6)))
# # 1

# # functools.reduce replacing custom lambda with operator.xor
# import operator
# print(functools.reduce(operator.xor, range(6)))
# # 1


# take a look at vector_v4; __eq__ and __hash__; two alternative methods for __eq__

# example - tests of hashing
# from Sec10_examples.vector_v4 import Vector

# v1 = Vector([3, 4])
# v2 = Vector([3.1, 4.2])
# v3 = Vector([3, 4, 5])
# v6 = Vector(range(6))
# print((hash(v1), hash(v3), hash(v6)))
# # (7, 2, 1)

# usage of zip(), learned about all()

''' 
more on zip()

makes it easy to iterate in parallel over two or more iterables by returning tuples you can unpack into variables, one for each item in the parallel inputs
'''
# # example - zip() at work

# # zip returns generator that produces tuple on demand
# print(zip(range(3), 'ABC'))
# # <zip object at 0x7fa421fdf0c8>

# # here we build a list from it just for display; usually we iterate over the generator
# print(list(zip(range(3), 'ABC')))
# # [(0, 'A'), (1, 'B'), (2, 'C')]

# # zip has a surprising trait: it stops without warning when one of the iterables is exhausted
# print(list(zip(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3])))
# # [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2)]

# # The itertools.zip_longest function behaves differently: it uses an optional fillvalue(None by default) to complete missing values so it can generate tuples until the last iterable is exhausted
# from itertools import zip_longest
# print(list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1)))
# # [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2), (-1, -1, 3.3)]


'''
Vector take #5: Formatting

instead of providing a custom display in polar coordinates like we did in Vector2d, Vector will use spherical coordinates (hyperspherical coordinates because we support N-dimensions and spheres are "hyperspheres" in 4D and beyond)
*change the 'p' to 'h'

A Vector object in 4D space (len(v) == 4), the 'h' code will display like so: <r, Φ1, Φ2, Φ3>, where r is the magnitude (abs(v)) and the remaining numbers are angular coordinates

before we start; we need to code a pair of support methods: angle(n) to compute one of the angular coordinates where angle() will return an iterable of all the angular coordinates
'''

# take a look at vector_v5; angle(), angles(), __format__

# example - tests of format() with cartesian coordinates in 2D:
# from Sec10_examples.vector_v5 import Vector

# v1 = Vector([3, 4])
# print(format(v1))
# # (3.0, 4.0)

# print(format(v1, '.2f'))
# # (3.00, 4.00)

# print(format(v1, '.3e'))
# # (3.000e+00, 4.000e+00)


# example - tests of format() with Cartesian coordinates in 3D and 7D
# from Sec10_examples.vector_v5 import Vector

# v3 = Vector([3, 4, 5])
# print(format(v3))
# # (3.0, 4.0, 5.0)

# print(format(Vector(range(7))))
# # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)


# tests of  format() with spherical coordinates in 2D, 3D and 4D
# from Sec10_examples.vector_v5 import Vector

# print(format(Vector([1, 1]), 'h'))
# # <1.4142135623730951, 0.7853981633974483>

# # scientific notation before 'h'
# print(format(Vector([1, 1]), '.3eh'))
# # <1.414e+00, 7.854e-01>

# # f notation before 'h'
# print(format(Vector([1, 1]), '0.5fh'))
# # <1.41421, 0.78540>

# print(format(Vector([1, 1, 1]), 'h'))
# # <1.7320508075688772, 0.9553166181245093, 0.7853981633974483>

# print(format(Vector([2, 2, 2]), '.3eh'))
# # <3.464e+00, 9.553e-01, 7.854e-01>

# print(format(Vector([0, 0, 0]), '0.5fh'))
# # <0.00000, 0.00000, 0.00000>

# print(format(Vector([-1, -1, -1, -1, -1]), 'h'))
# # <2.23606797749979, 2.0344439357957027, 2.0943951023931957, 2.186276035465284, 3.9269908169872414>

# print(format(Vector([2, 2, 2, 2]), '.3eh'))
# # <4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>

# print(format(Vector([0, 1, 0, 0]), '0.5fh'))
# # <1.00000, 1.57080, 0.00000, 0.00000>