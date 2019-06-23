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
#         # for this demonstratioon, __getitem__ merely returns whatever is passed to it
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

# example - part of vector_v2.py: __len__ and __getitem__ methods have been added to Vector class from vector_v1.py