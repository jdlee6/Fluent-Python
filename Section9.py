'''
A Pythonic Object

Object representations
Python has 2 ways of getting a string representation: 
    repr(): return a string representing the object as the DEV wants to see it
    str(): return a string representing theo bejct as the USER wants to see it
    *implemented __repr__ and __str__ to support the methods above

    __bytes__: analagous to __str__, called by bytes() to get the object represented as a BYTE sequence
    __format__: format() and str.format() methods call it to get string displays of objects using special formatting codes

Vector class redux
Look at the example below
'''
# example continued - class Vector2d
from array import array
import math

class Vector2d:
    # type code is a class attribute we'll use when converting Vector2d instances to/from bytes
    typecode = 'd'

    def __init__(self, x, y):
        # Converting x and y to float in __init__ catches errors early, in case Vector2d is called with unsuitable arguments
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        # __iter__ makes a Vector2d iterable; this is what makes unpacking work, e.g., x, y = my_vector
        # we implement it simply by using a generator expression to yield the components one after the other
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        # __repr__ builds a string by interpolating the compoents with {!r} to get their repr; because Vector2d is iterable, *self feeds the x and y components to format
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self)) 


# example - Vector2d instances have several representations
v1 = Vector2d(3, 4)
# The components of a Vector2d can be accessed directly as attributes (no getter method calls)
print(v1.x, v1.y)
# 3.0 4.0

x, y = v1
print(x, y)
# 3.0 4.0

print(v1)
# (3.0, 4.0)

v1_clone = eval(repr(v1))
print(v1 == v1_clone)
# True

print(v1)
# (3.0, 4.0)

octets = bytes(v1)
print(octets)
# b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'

print(abs(v1))
# 5.0

print(bool(v1), bool(Vector2d(0, 0)))
# True False

