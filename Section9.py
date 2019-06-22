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


# examples - look at vector2d_instances.py and then look at vector2d_v0.py for the class object information


'''
one obvious operation is missing: rebuilding a Vector2d from the binary representation produced by bytes()

Alternative constructor

we can export Vector2d as bytes so we need a method that imports a Vector2d from a binary sequence
array.array has a class method named .frombytes
'''


# example - look at vector2d_v1.py
# in the last line, notice how cls argument is invoked to build a new instance: cls(*memv)


'''
classmethod vs. static method

classmethod (shown in the example above) is used to define a method that operates on the class and NOT on instances.           -change the way the method is called, so it receives the class itself as the first argument, instead of an instance
    -common use: alternate constructors 

staticmethod decorator changes a method so it receives no special first argument
    -like a plain function that happens to live in a class body, instead of being defined at module level

** if you want to define a function that does not interact with the class; just define it in the module hence no need for staticmethod decorators
'''
# example - comparing behaviors of classmethod and static method

# class Demo:
#     @classmethod
#     def klassmeth(*args):
#         # klassmeth just returns all positional arguments
#         return args

#     @staticmethod
#     def statmeth(*args):
#         # statmeth does the same
#         return args

# # no matter how you invoke it, Demo.klassmeth receives the Demo class as the first argument
# print(Demo.klassmeth())
# # (<class '__main__.Demo'>,)

# # Demo.statmeth behavese just like a plain old function
# print(Demo.klassmeth('spam'))
# # (<class '__main__.Demo'>, 'spam')

# print(Demo.statmeth())
# # ()

# print(Demo.statmeth('spam'))
# # ('spam',)


'''
formatted displays

format() built-in function and the str.format() method delegate the actual formatting to each type by calling their .__format__(format_spec) method

format_spec is a formatting specifier:
    -second argument in format(my_obj, format_spec)
    -whatever appears after the colon in a replacement field delimited with {} inside a format string used with str.format()

format string such as {0.mass:5.3e} uses two separate notations:
    the '0.mass' to the left of the colon is the field_name part of the replace field syntax;
    the '5.3e' after the colon is the formatting specifier
'''
# example 
# brl = 1/2.43
# print(brl)
# # 0.4115226337448559

# # formatting specifier is '0.4f'
# print(format(brl, '0.4f'))
# # 0.4115

# # formatting specifier is '0.2f'. The 'rate' substring in the replacement field is called the field name. It's unrelated to the formatting specifier, but determines which argument of .format() goes into that replacement field.
# print('1 BRL = {rate:0.2f} USD'.format(rate=brl))
# # 1 BRL = 0.41 USD


'''
few built-in types have their own presentation codes 
    - the int type supports b and x for base 2 and base 16 output
    - float implements f for a fixed point display and % for a percentage display:

https://docs.python.org/3/library/string.html#formatspec
Format Specification Mini-Language is extensible b/c each class gets to interpret the format spec argument as it likes
    i.e. - classes in the datetime module use the SAME format codes in strftime() and in their __format__ methods
'''
# print(format(42, 'b'))
# # 101010

# print(format(2/3, '.1%'))
# # 66.7%

# from datetime import datetime
# now = datetime.now()
# print(format(now, '%H:%M:%S'))
# # 16:15:03

# # %I = Hour (12 hour clock) as a zero padded decimal number
# # %p = Locale's equivalent of either AM or PM
# # notice how we used an f-string; we can use .format as well
# print(f"It\'s now {now:%I:%M %p}")
# # print("It's now {:%I:%M %p}".format(now))
# # It's now 04:16 PM


# if a class has NO __format__, the method inherite from object returns str(my_object)
# since Vector2d has a __str__, this works:

# from Sec9_examples.vector2d_v0 import Vector2d

# v1 = Vector2d(3, 4)
# print(format(v1))
# # (3.0, 4.0)


# however if you pass a format specifier, object.__format__ raises TypeError:
# print(format(v1, '.3f'))
# # TypeError: unsupported format string passed to Vector2d.__format__

'''
to fix the problem above; we will implement our own format mini-language
    1. assume the format specifier provided by the user is intended to format each float component of the vector

before we attempt the tests below: make sure to look at the def __format__(self, fmt_spec=' '): in vector2d_v0.py
'''
# v1 = Vector2d(3, 4)
# print(format(v1))
# # (3.0, 4.0)

# print(format(v1, '.2f'))
# # (3.00, 4.00)

# print(format(v1, '.3e'))
# # (3.000e+00, 4.000e+00)

'''
let's add a custom formatting code:
    if the format specifier ends with a 'p', we'll display the vector in polar coordinate: <r, θ> 
        -r is the magnitude, θ (theta) is the angle in radians

*take a look at class Vector2d in vector2d_v0.py
'''
# print(format(Vector2d(1, 1), 'p'))
# # (1.4142135623730951, 0.7853981633974483)

# print(format(Vector2d(1, 1), '.3ep'))
# # (1.414e+00, 7.854e-01)

# print(format(Vector2d(1,1), '0.5fp'))
# # (1.41421, 0.78540)


'''
make our Vector2d hashable - so we can build sets of vectors or use them as dict keys
BEFORE we do this, we MUST make vectors immutable


A hashable Vector2d

Vector2d instances are unhashable so we can't put them in a set
    -see the example below

to make a Vector2d hashable, we must implement __hash__ 
*__eq__ is also required but we already defined that in our Vector2d class object

we also have to make vector instances IMMUTABLE
'''
# from Sec9_examples.vector2d_v0 import Vector2d

# v1 = Vector2d(3, 4)
# print(hash(v1))
# # TypeError: unhashable type: 'Vector2d'

# print(set([v1]))
# # TypeError: unhashable type: 'Vector2d'

# print((v1.x, v1.y))
# # (3.0, 4.0)

# in addition to implementing __hash__; we will have to make vector instances immutable
# v1.x = 7
# # we want this error below to pop up
# # AttributeError: can't set attribute

'''
take a look at vector2d_v3.py

now we can implement the __hash__ method which should return an int and take into account the hashes of the object attributes that are also used in the __eq__ method (objects compare equal if they share the same hash)
    -bitwise xor operator (^) is used to mix hashes of the components

take a look at vector2d_v3.py for the additional changes and vector2d_v0.py for the full class object
'''

# from Sec9_examples.vector2d_v0 import Vector2d

# v1 = Vector2d(3, 4)
# v2 = Vector2d(3.1, 4.2)
# print((hash(v1), hash(v2)))
# # (8777760545144, 8777759234368)

# print(set([v1, v2]))
# # {<Sec9_examples.vector2d_v0.Vector2d object at 0x7fd7f8518780>, <Sec9_examples.vector2d_v0.Vector2d object at 0x7fd7f7119400>}

# print(set(v1))
# # TypeError: 'Vector2d' object is not iterable

'''
__int__ and __float__ methods may be useful for sensible scalar numeric values which are invoked by int() and float() constructors
__complex__ method supports the complex() built-in constructor

take a look at page 259 for the compiled examples with Vector2d class:
tests of instances; tests of .frombytes() class method; tests of format() with Cartesian coordinates; tests of the angle method; tests of format() with polar coordinates; tests of 'x' and 'y' read-only properties; tests of hashing 


Private and "protected" attributes in Python

No way to create private variables in Python but we do have a simple mechanism to prevent accidental overwriting of a "private" attribute in a subclass

example:
class Dog - uses mood instance attribute INTERNALLY, without exposing it and then subclass that Dog as Beagle
    -if you create your own instance attribute, mood, without being aware of the name clash; you will clobber the mood attribute used by the methods inherited from Dog

*prevent this by using an instance attribute in the form __mood (two leading underscores and zero or at most one trailing underscore)
    -__mood becomes _Dog__mood and in Beagle it would be _Beagle__mood

name mangling is about SAFETY and designed to prevent accidental access and NOT intentional wrong doing

See the example below
'''
# example - pivate attribute names are "mangled" by prefixing the _ and the class name

# from Sec9_examples.vector2d_v0 import Vector2d

# v1 = Vector2d(3, 4)
# print(v1.__dict__)
# # {'_Vector2d__x': 3.0, '_Vector2d__y': 4.0}

# # useful for debugging and serialization
# print(v1._Vector2d__x)
# # 3.0

'''
attributes with a single _ prefix are called "protected"
-practice is widespread, but calling a "protected attribute" is NOT so common

conclusion:
Vector2d components are "private" and our Vector2d instances are "immutable"


Saving space with the __slots__ class attribute

by default; Python stores instance attributes in a per-instance dict named __dict__
    -dictionaries have SIGNIFICANT memory overhead 

if you are dealing with millions of instances with few attributes, the __slots__ class attribute can SAVE a lot of memory by letting the interpreter store the instance attributes in a TUPLE instead of a DICT
    -to define __slots__: create a class attribute with that name and assign it an iterable of str with identifiers for the instance attributes
'''
# example - take a look at vector2d_v3_slots.py

'''
now instead of storing the instance attributes in a dictionary, it will now store them in a tuple-like structure 
    -makes a huge difference in memeory usage if you have millions of instances active at the same time

look at the example below
'''

# example (DEMO page 266) - mem_test.py - creates 10 million Vector2d instances using the class defined in the named module 

#  $ time python3 mem_test.py vector2d_v3.py
# Selected Vector2d type: vector2d_v3.Vector2d
# Creating 10,000,000 Vector2d instances

# Initial RAM usage:
# 5,623,808
# Final RAM usage: 1,558,482,944

# real 0m16.721s
# user 0m15.568s
# sys 0m1.149s

# $ time python3 mem_test.py vector2d_v3_slots.py
# Selected Vector2d type: vector2d_v3_slots.Vector2d
# Creating 10,000,000 Vector2d instances

# Initial RAM usage:
# 5,718,016
# Final RAM usage:
# 655,466,496

# real 0m13.605s
# user 0m13.163s
# sys 0m0.434s

'''
in the example above; you can see that the final RAM usage has significantly decreased and also that __slots__ verion is faster

the mem_test.py script deals with loading a module, checking memory usage and formatting results

another special per-instance attribute is __weakref__ attribute which is necessary for an object to support weak references
    -present by default in instances of user-defined classes

BUT if class defines __slots__ and you need the instances to be targets of weak references; then you need to INCLUDE __weakref__ among the attributes named in __slots__


The PROBLEMS with __slots__
    -must remember to redeclare __slots__ in each subclass, since the inherited attribute is ignored by the interpreter
    -instances will only be able to have the attributes listed in __slots__ unless you include __dict__ in __slots__ - doing it like this may be counter effective
    -instances CANNOT be targets of weak references unless you rememer to include __weakref__ in __slots__


Overriding class attributes

refer to our Vector2d example:
    -typecode is the default class attribute
    -instance retreive the default class attribute by accessing it via self.typecode

*if you write to an instance attribute that does NOT exist, you create a new instance attribute (i.e. typecode instance attribute)
    -when the code tries to read self.typecode it will read from the instance attribute (typecode) which ends up shadowing the class attrbute typecode

look at the example below
'''
# example - customizing an instance by setting the typecode attribute that was formerly inherited from the class

from Sec9_examples.vector2d_v0 import Vector2d

v1 = Vector2d(1.1, 2.2)
dumpd = bytes(v1)
print(dumpd)
# b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@'

# default bytes representation is 17 bytes long
print(len(dumpd))
# 17

# set typecode to 'f' in the v1 instance
v1.typecode = 'f'
dumpf = bytes(v1)
print(dumpf)
# b'f\xcd\xcc\x8c?\xcd\xcc\x0c@'

# now the bytes dump is 9 bytes long
print(len(dumpf))
# 9

# Vector2d.typecode is unchanged, only the v1 instance uses typecode 'f'
print(Vector2d.typecode)
# d

'''
if you want to change a class attribute - you must set it on the class DIRECTLY and NOT through an instance 
-to change the default typecode for instances you can do something similar to the example above: v1.typecode = 'f'

subclass to customize a class data attribute that is inherited
'''
# example - the ShortVector2d is a subclass of Vector2d which only overwrites the default type code

from Sec9_examples.vector2d_v0 import Vector2d

# Create ShortVector2d as a Vector2d subclass just to overwrite the typecode class attribute
class ShortVector2d(Vector2d):
    typecode = 'f'

# build ShortVector2d instance sv for demonstration
sv = ShortVector2d(1/11, 1/27)

# inspect the repr of sv
print(repr(sv))
# ShortVector2d(0.09090909090909091, 0.037037037037037035)

# check the length of the exported bytes is 9 and NOT 17
print(len(bytes(sv)))
# 9

'''
also take note that we didn't hardcode the class name which would have prevented us from seeing 'ShortVector2d ... ' when we created subclasses that inherit from class Vector2d
'''
