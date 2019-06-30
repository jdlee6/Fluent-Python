'''
Operator Overloading allows user-defined objects to interoperate with infix operators such as + and | or unary operators like - and ~


Operator Overloading 101
**language feature that can be abused, resulting in programmer confusion, bugs and performance bottlenecks

Limitations:
    -Cannot overload operators for the built-in types
    -Cannot create new operators, only overload existing ones
    -Few operators can't be overloaded: is, and, or, not (but the bitwise &, |, ~ can)

Rich comparison operators (== != > < >= <=) are special cases in operator overloading are SPECIAL cases


Unary operators
https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations
    - __neg__: Arithmetic unary negation. If x is -2 then -x == 2
    + __pos__: Arithmetic unary plus. Usually x == +x, but there are a few cases when that is NOT true
    ~ __invert__: Bitwise inverse of an integer, defined as ~x == -(x+1). If x is 2 then ~x == -3

    How to support? Implement the appropriate special method, which will receive just ONE argument: self
        *Always return a new object
'''
# example - take a look at vector_v6.py (__neg__ and __pos__)

# example - a change in the arithmetic context precision may cause x to differ from +x [usually equal value except a rare case like the one below]

# import decimal
# # get a reference to the current global arithmetic context
# ctx = decimal.getcontext()
# # set precision of the arithmetic context to 40
# ctx.prec = 40
# # compute 1/3 using the current precision
# one_third = decimal.Decimal('1') / decimal.Decimal('3')
# # inspect the result; there are 40 digits after the decimal point
# print(repr(one_third))
# # Decimal('0.3333333333333333333333333333333333333333')

# # one_third == +one_third is True
# print(one_third == +one_third)
# # True

# # lower precision to 28 - the default for Decimal arithmetic in Python3.4
# ctx.prec = 28
# # Now one_third == +one_third is False
# print(one_third == +one_third)
# # False

# # inspect +one_third; there are 28 digits are the '.' here
# print(repr(+one_third))
# # Decimal('0.3333333333333333333333333333')

# each occurrence of the expression +one_third produces a new Decimal instance from the value of one_third but using the precision of the current arithmetic context

# example - unary + produces a new Counter without zeroed or negative tallies
# from collections import Counter

# ct = Counter('abracadabra')
# print(ct)
# # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# ct['r'] = -3
# ct['d'] = 0

# print(ct)
# # Counter({'a': 5, 'b': 2, 'c': 1, 'd': 0, 'r': -3})

# # discards any negative or zero count valued keys
# # + produces a new counter preserving only the tallies that are greater than zero
# print(+ct)
# # Counter({'a': 5, 'b': 2, 'c': 1})


'''
Overloading + for vector addition

Vector class is a SEQUENCE type and the Data model says the sequences should support the + operator for concatenation and * for repetition

In the example below, we will implement + and * as MATHEMATICAL vector operations
'''
# take a look at vector_v6; __add__
# from Sec13_examples.vector_v6 import Vector

# v1 = Vector([3, 4, 5])
# v2 = Vector([6, 7, 8])
# print(repr(v1+v2))
# # TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector' (without __add__)
# # Vector([9.0, 11.0, 13.0])

# print(v1 + v2 == Vector([3+6, 4+7, 5+8]))
# # True

# v3 = Vector([3, 4, 5, 6])
# v4 = Vector([1, 2])
# print(repr(v3+v4))
# # Vector([4.0, 6.0, 5.0, 6.0])


# example - vector_v6 __add__ take #1 supports non-Vector objects too
# from Sec13_examples.vector_v6 import Vector

# v1 = Vector([3, 4, 5])
# print(repr(v1 + (10, 20, 30)))
# # Vector([13.0, 24.0, 35.0])

# from Sec9_examples.vector2d_v0 import Vector2d

# v2d = Vector2d(1, 2)
# print(repr(v1 + v2d))
# # Vector([4.0, 6.0, 5.0])

'''
both additions in the example work because __add__ uses zip_longest(...), which can consume ANY iterable and the generator expression to build the new Vector merely performs a + b with the pairs produced by zip_longest(...), so an iterable producing any number items will do
'''

# example - vector_v6 __add__ take #1 fails with NON-Vector left operands
# from Sec13_examples.vector_v6 import Vector
# v1 = Vector([3, 4, 5])
# print(repr((10, 20, 30) + v1))
# # TypeError: can only concatenate tuple (not "Vector") to tuple

# from Sec9_examples.vector2d_v3 import Vector2d
# v2d = Vector2d(1, 2)
# print(repr(v2d + v1))
# # TypeError: unsupported operand type(s) for +: 'Vector2d' and 'Vector'

'''
To support operations involving objects of different types, Python implements a special dispatching mechanism for the infix operator special methods. 

The interpreter will perform these steps below for the expression: a + b
    1. if a has __add__, call a.__add__(b) and return result unless it's NotImplemented
    2. if a doesn't have __add__, or calling it returns NotImplemented, check if b has __radd__, then call b.__radd__(a) and return result unless it's NotImplemented
    3. If b doesn't have __radd__ or calling it returns NotImplemented, raise TypeError with an 'unsupported operand types' message
*__radd__ method is called "reflected" or "reversed" or "right" (called on right hand operand)

To make the mixed-type addition in the example above work, we need to implement the Vector.__radd__ method which will be a fall back if the left operand does NOT implement __add__ or if it does but returns NotImplemented to signal that doesn't know how to handle the right operand
'''
# example - take a look at vector_v6.py __add__ and __radd__ methods

# example - vector_v6.py test fail - operand is iterable but its items cannot be added to the float items in the Vector
# from Sec13_examples.vector_v7 import Vector

# v1 = Vector([1, 2, 3])
# print(repr(v1 + 1))
# # TypeError: zip_longest argument #2 must support iteration

# # example - vector_v6.py test fail - __add__ method needs an iterable with numeric items
# print(repr(v1+'ABC'))
# # TypeError: unsupported operand type(s) for +: 'float' and 'str'

'''
if an operator special method CANNOT return a valid result b/c of type incompatibilty, it should return NotImplemented instead of raising a TypeError

In the a case of TypeError, it is better to catch it and return NotImplemented which allows the interpreter to try calling the REVERSED operator method which may correctly handle the computation with swapped operands if they are of different types
    if this fails then it will indeed return a TypeError
'''

# example - take a look at vector_v7.py - operator + methods added to vector_v6.py

'''
Overloading * for scalar multiplication

Vector([1, 2, 3]) * x; if x is a number that would be a scalar product and the result would be a new Vector with each component multiplied by x (this is known as Elementwise Multiplication)

Another kind of product involving Vector operands would be the dot product of two vectors aka Matrix Multiplication
    ie. numpy.dot()
    https://www.tutorialspoint.com/numpy/numpy_dot.htm
'''

#  we would like the following to happen
# from Sec13_examples.vector_v7 import Vector

# v1 = Vector([1, 2, 3])
# print(v1 * 10)
# # TypeError: unsupported operand type(s) for *: 'Vector' and 'int'
# # Vector([10.0, 20.0, 30.0])

# example - vector_v8.py __mul__ and __rmul__ - we can now multiply Vectors by scalar values of the usual and not so usual numeric types
# from Sec13_examples.vector_v8 import Vector

# v1 = Vector([1.0, 2.0, 3.0])
# print(repr(14 * v1))
# # Vector([14.0, 28.0, 42.0])

# print(repr(v1 * True))
# # Vector([1.0, 2.0, 3.0])

# from fractions import Fraction
# print(repr(v1 * Fraction(1, 3)))
# # Vector([0.3333333333333333, 0.6666666666666666, 1.0])

'''
the methods above are applicable to all the operators in Section13.txt

*Rich comparison operators are another category for infix operators, using a slightly different set of rules
'''

# # example - vector_v8.py; @ operator (__matmul__); matrix multiplication
# from Sec13_examples.vector_v8 import Vector

# va = Vector([1, 2, 3])
# vz = Vector([5, 6, 7])
# # 1*5 + 2*6 + 3*7
# print(va @ vz == 38.0)
# # True


'''
Rich comparison operators

Handling of the rich comparison operators == != > < >= <= DIFFERS in 2 important aspects
    1. same set of methods are used in forward and reverse operator calls; rules are summarized in Section13.txt
    2. in the case of == and !=, if the reverse call fails, Python compares the object ids instead of raising TypeError
'''

# example - vector_v9; __eq__ - Comparing a Vector a Vector, a Vector2d and a tuple
# from Sec13_examples.vector_v9 import Vector

# va = Vector([1.0, 2.0, 3.0])
# vb = Vector(range(1, 4))
# # Two Vector instances with equal numeric components compare equal
# print(va == vb)
# # True

'''
This is what happens in the Vector2d comparison example:
    1. to evaluate vc == v2d, Python calls Vector.__eq__(vc, v2d)
    2. Vector.__eq__(vc, v2d) verifies that v2d is NOT a Vector and returns NotImplemented
    3. Python gets NotImplemented result, so it tries Vector2d.__eq__(v2d, vc)
    4. Vector2d.__eq__(v2d, vc) turns BOTH operands into tuples and compares them: the result is True 
        *take a look at vector2d_v0.py __eq__ method
'''

# from Sec9_examples.vector2d_v0 import Vector2d
# vc = Vector([1, 2])
# v2d = Vector2d(1, 2)
# # A Vector and a Vector2d are also equal if their components are equal
# print(vc == v2d)
# # True

'''
In the Vector and Tuple example, this is what happens
    1. to evaluate va == t3, Python calls Vector.__eq__(va, t3)
    2. Vector.__eq__(va, t3) verifies that t3 is NOT a Vector and returns NotImplemented
    3. Python gets NotImplemented result so it tries tuple.__eq__(t3, va)
    4. tuple.__eq__(t3, va) has no idea what a Vector is, so it returns NotImplemented
    5. In the special case of ==; if the reverse call returns NotImplemented then Python compares the object ids as a last resort

**when __eq__ is defined and does not return NotImplemented, __ne__ returns that result NEGATED
**__ne__ is inherited from the object class and there is rarely a case to override it 
'''

# t3 = (1, 2, 3)
# # Why does this return False?
# print(va == t3)
# # False


# # example - results for !=
# print(va != vb)
# # False

# print(vc != v2d)
# # False

# print(va != (1, 2, 3))
# # True

'''
Augmented Assignment Operators
'''
# example - Augmented assignment works with immutable targets by creating new instances and rebinding
# from Sec13_examples.vector_v9 import Vector

# v1 = Vector([1, 2, 3])
# # create alias so we can inspect the Vector([1, 2, 3]) object later
# v1_alias = v1

# # remember the id of the initial Vector bound to v2
# print(id(v1))
# # 140482469308064

# # Perform augmented addition
# v1 += Vector([4, 5, 6])
# # Expected result
# print(repr(v1))
# # Vector([5.0, 7.0, 9.0])

# # but a new Vector was created
# print(id(v1))
# # 140482448335872

# # Inspect v1_alias to confirm the original Vector was not altered
# print(repr(v1_alias))
# # Vector([1.0, 2.0, 3.0])

# # perform augmented multiplication
# v1 *= 11
# print(repr(v1))
# # Vector([55.0, 77.0, 99.0])

# # the result is a NEW Vector that was created
# print(id(v1))
# # 140482469308288

'''
if a class does NOT implement the in-place operators listed in Section13.txt, the augmented assignment operators are just syntactic sugar: a += b is evaluated exactly as a = a + b
    *if  __add__ is defined then += will work with no additional code

however if you implement __iadd__, then that method is called to compute the result of a += b; these operators are expected to CHANGE the left hand operand in-place and NOT create a new object as the result
'''
# example - extend bingocage.py class and implement __add__ and __iadd__ in bingoaddable.py
# a new AddableBingoCage subclass instance can be created with +

from Sec13_examples.bingoaddable import AddableBingoCage

vowels = 'AEIOU'
# Create a globe instance with 5 items (each of the vowels)
globe = AddableBingoCage(vowels)
print(globe.inspect())
# ('A', 'E', 'I', 'O', 'U')

# Pop one of the items and verify it is one the vowels
print(globe.pick() in vowels)
# True

# Confirm that the globe is down to 4 items
print(len(globe.inspect()))
# 4

# Create a second instance, with 3 items
globe2 = AddableBingoCage('XYZ')
globe3 = globe + globe2
# Create a third instance by adding the previous two. This instance will have 7 items
print(len(globe3.inspect()))
# 7

# Attempting to add an AddableBingoCage to a list fails with TypeError. That error message is produced by the Python interpreter when our __add__ method returns NotImplemented
# void = globe + [10, 20]
# # TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'

# example - An existing AddableBingoCage can be loaded with += (continued from example above)
# Create an alias so we can check the identity of the object later
globe_orig = globe
# globe has 4 items here
print(len(globe.inspect()))
# 4

# an AddableBingoCage instance can receive items from another instance of the same class
globe += globe2
print(len(globe.inspect()))
# 7

# the right hand operand of += can also be of ANY iterable
globe += ['M', 'N']
print(len(globe.inspect()))
# 9

# throughout this example; globe has always referred to the globe_orig project
print(globe is globe_orig)
# True

# trying to add a non-iterable to an AddableBingoCage fails with a proper error message
# globe += 1
# # TypeError: right operand in += must be 'AddableBingoCage' or an iterable

'''
note: += operator is MORE liberal than + in regards to the second operand
+ we want both operands to be of the same type AddableBingoCage
    if different types -> might cause confusion to the type of the result

+= situation is clearer: the left hand object is updated in-place so there's NO doubt about the type of result

Contrast the return statements that produce results in __add__ and __iadd__:
__add__
    the result is produced by calling the constructor AddableBingoCage to build a new instance

    ** Note: we didn't implement __radd__ here because there is NO need for it
        *if a (AddableBingoCage) and b (is not) are different types, it will return NotImplemented and we should let Python raise a TypeError because we cannot handle b
        ***if a forward infix operator is designed to work only with SAME types; it is useless to implement the reverse method

__iadd__
    the result is produced by returning self, after it has been modified
'''