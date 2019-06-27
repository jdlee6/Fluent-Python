'''
Interfaces: from protocols to ABCs

*only a very small minority of Python devs an create ABCs without imposing unreasonable limitations and needless work on fellow programmers


Interfaces and protocols in Python culture
1. every class has an interface: the set public attributes (methods or data attributes) implemented or inherited by the class
    -includes special methods

*private and protected attributes are NOT part of an interface
    -can have a data attribute as part of the interface of an object because they can be turned into a property by implementing getter/setter logic (look at the example below)
'''
# example - vector2d_v0.py: x and y are public data attributes (same code as section 9 example)

# class Vector2d:
#     typecode = 'd'

#     def __init__(self, x, y):
#         self.x = float(x)
#         self.y = float(y)

#     def __iter__(self):
#         return (i for i in (self.x, self.y))


# example - vector2d_v3.py: x and y reimplemented as properties (same code as section 9 example)

# class Vector2d:
#     typecode = 'd'

#     def __init__(self, x, y):
#         self.__x = float(x)
#         self.__y = float(y)

#     @property
#     def x(self):
#         return self.__x

#     @property
#     def y(self):
#         return self.__y

#     def __iter__(self):
#         return (i for i in (self.x, self.y))

'''
interface: the subset of an object's public methods that enable it to play a specific role in the system
protocol: interface seen as a set of methods to fulfill a role; independent of inheritance
    -defined only by documentation and convention
    -can be partially implemented in a particular class


Python digs sequences
'''
# # example - Partial sequence protocol implementation with __getitem__: enough for item access, iteration and the in operator
# class Foo:
#     def __getitem__(self, pos):
#         return range(0, 30, 10)[pos]

# f = Foo()
# print(f[1])
# # 10

# for i in f:
#     print(i)
# # 0
# # 10
# # 20

# print(20 in f)
# # True

# print(15 in f)
# # False

'''
notice how there is no __iter__ method yet the instances are iterable; this is bc Python sees the __getitem__ method
the in method works as well even though there is NO __contains__ method

so even with the absence of __iter__ and __contains__; Python still manages to make iteration and the in operator work by invoking __getitem__

the FrenchDeck example from Chapter 1 implements BOTH methods of the sequence protocol: __getitem__ and __len__
'''

# example - a deck as a sequence of cards
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


'''
Monkey-Patching to implement a protocol at run time

if the class acts like a sequence then it doesn't need a shuffle method because there is already a random.shuffle method

'''
# # random.shuffle
# from random import shuffle
# l = list(range(10))
# shuffle(l)
# print(l)
# # [5, 4, 8, 0, 1, 7, 6, 3, 2, 9]

# example - random.shuffle CANNOT handle FrenchDeck
# from random import shuffle

# deck = FrenchDeck()
# shuffle(deck)
# # TypeError: 'FrenchDeck' object does not support item assignment

'''
random.shuffle operates by swapping items INSIDE the collection and FrenchDeck only implements the IMMUTABLE sequence protocol
*mutable sequences must also provide a __setitem__ method
'''

# example - Monkey patching FrenchDeck to make it mutable and compatible with random.shuffle 
# from random import shuffle

# deck = FrenchDeck()

# # create a function that takes deck, position, and card as arguments
# def set_card(deck, position, card):
#     deck._cards[position] = card

# # assign that function to an attribute named __setitem__ in the FrenchDeck class
# FrenchDeck.__setitem__ = set_card

# # deck can now be sorted because FrenchDeck now implements the necessary method of the MUTABLE sequence protocol
# shuffle(deck)
# print(deck[:5])
# # [Card(rank='K', suit='diamonds'), Card(rank='3', suit='diamonds'), Card(rank='9', suit='hearts'), Card(rank='Q', suit='diamonds'), Card(rank='2', suit='clubs')]

'''
set_card knows that the deck object has an attribute named _cards and _cards MUST be a mutable sequence
set_card function is then attached to the FrenchDeck class as the __setitem__ special method
    example of monkey patching: changing a class or module at run time without touching the source code

protocols are dynamic: random.shuffle doesn't care what type of argument it gets, it only needs the object to implement part of the mutable sequence protocol


ABCs - Abstract Base Class

inheriting from an ABC is more than implementing the required methods - it's a clear declaration of intent by the developer

the use of isinstance and issubclass is more acceptable to test against ABCs
    -excessive use of the two is bad code design

OK to do isinstance/subclass checks against an ABC if it needs enforcement

restrain yourself from creating an ABC - just use the existing ones correctly to avoid serious risk of mis-design
'''
# example - code snippet example of duck typing to handle a string or an iterable of strings (instead of using isinstance)

# # assume it's a string (EAFP = it's easier to ask forgiveness than permission)
# try:
#     # Convert commas to spaces and split the result into a list of names
#     field_names = field_names.replace(',',' ').split()
#     print(field_names)
# # Sorry, field_names doesn't quack like a str ... there's either no .replace or it returns something we can't split
# except AttributeError:
#     # Now we assume it's already an iterable of names
#     pass

# # to make sure it's an iterable and to keep our own copy, create a tuple out of what we have
# field_names = tuple(field_names)


'''
Subclassing an ABC

Python only checks for the implementation of the abstract methods only at run time when we try to instantiate FrenchDeck2
If we failed to implement any abstract method - we would receive a TypeError exception; the MutableSequence ABC demands these methods

In order to use ABCs well you will NEED to know what is available . . .
'''

# # example - take a look at frenchdeck2.py 

# from Sec11_examples.frenchdeck2 import FrenchDeck2

# f = FrenchDeck2()
# print(list(f))


'''
ABCs in the standard library

ABCs in collections.abc
https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

16 ABCs defined in collections.abc (figure 11-3)

Clusters:
    i. Iterable, Container and Sized: 
        Every collection should either inherit from these ABCs or at least implement compatible protocols. Iterable supports iteration with __iter__; Container supports the in operator with __contains__; Sized supports len() with __len__

    ii. Sequence, Mapping, and Set
        These are the main immutable collection types and each has a mutable subclass. 

    iii. MappingView
        In Python 3, the objects returned from the mapping methods .items() .keys() and .values() inherit from ItemsView, KeysView, and ValuesView respectively; first 2 inherit from Set

    iv. Callable and Hashable
        Rare to see subclasses of Callable/Hashable. Their main use is to support isinstance built-in as a safe way of determining whether an object is callable or hashable

    v. Iterator
        Note that iterator subclasses Iterable.


The numbers tower of ABCs

https://docs.python.org/3/library/numbers.html

Number is the topmost superclass, Complex is its immediate subclass and so on, down to Integral.
    -Number; Complex; Real; Rational; Integral

isinstance(x, numbers.Integral) to accept int, bool (which subclasses int) or other integer types that may be provided by external libraries which register their types with the numbers ABCs

if you want a value to be a floating point type, write isinstance(x, numbers.Real) and your code will be happy to take bool, int, float, fractions.Fraction 


Defining and using an ABC

Problem: Need to build an ad management framework to display ads in random order without repeating an ad before the full inventory of ads is shown
    -to make it clear to users what is expect of a "non-repeating random-picking" component, we'll define an ABC
        ABC consists of four methods; the 2 abstract methods are:
            1. .load(...): put items into the container
            2. .pick(): remove one item at random from the container, returning it

        The concrete methods are:
            1. .loaded(): return True if there is at least one item in the container
            2. .inspect(): return a sorted tuple built from the items currently in the container without changing its contents (its internal ordering is not preserved)

*abstract methods can have an implementation - subclasses will still be forced to override it but they will invoke the abstract method with super() which will add functionality to it instead of implementing from scratch.
*ok to provide concrete methods in ABCs as long as they only depend on other methods in the interface
'''
# example - tombola.py - Tombola is an ABC with two abstract methods and two concrete methods

'''
LookupError is the Exception we handle in Tombola.inspect
IndexError is the LookupError subclass raised when we try to get a item from a sequence with an index beyond the last position
KeyError is raised when we use a non-existent key to get an item from a mapping
'''

# # example - fake Tombola doesn't go undetected
# # print(dir('Fake'))

# from Sec11_examples.tombola import Tombola

# # Declare Fake as a subclass of Tombola
# class Fake(Tombola):
#     def pick(self):
#         return 13

# # The class was created, no errors so far
# print(Fake)
# # <class '__main__.Fake'>

# print(Fake.__bases__[0].__bases__)
# # <class 'abc.ABC'>

# print(issubclass(Fake, Tombola))
# # True

# print(isinstance(Fake, type))
# # True

# print(Tombola.__mro__)
# # (<class 'Sec11_examples.tombola.Tombola'>, <class 'abc.ABC'>, <class 'object'>)

# # TypeError is raised when we try to instantiate Fake. The message is clear: Fake is considered abstract because it failed to implement load, one of the abstract methods declared in the Tombola ABC
# f = Fake()
# print(f)
# # TypeError: Can't instantiate abstract class Fake with abstract methods load


'''
ABC syntax details

best way to declare an ABC is to subclass abc.ABC or any other ABC
*'regular' classes don't check subclasses (special behavior of ABCs)

stacked decorators look like the example below
    *when abstractmethod() is applied in combination with other method descriptors, it should be applied in the innermost decorator
        *no other decorator should appear between @abstractmethod and the def statement
'''
# # example - stacked decorators with ABCs
# class MyABC(abc.ABC):
#     @classmethod
#     @abc.abstractmethod
#     def an_abstract_classmethod(cls, ...):
#         pass


'''
Subclassing the Tombola ABC
'''
# from Sec11_examples.tombola import Tombola
# import random

# # BingoCage class explicitly extends Tombola
# class BingoCage(Tombola):
#     def __init__(self, items):
#         # Pretend we'll use this for online gaming. random.SystemRandom implements the random API on top of the os.urandom(...) function which provides random bytes "suitable for cryptographic"
#         # SystemRandom class uses the system function os.urandom() to generate random numbers from sources provided
#         self._randomizer = random.SystemRandom()
#         self._items = []
#         # Delegate the initial loading to the .load() method
#         self.load(items)

#     def load(self, items):
#         self._items.extend(items)
#         # Instead of the plain random.shuffle() function, we use the .shuffle() method of our SystemRandom instance
#         self._randomizer.shuffle(self._items)

#     # pick is implemented as in Section 5 example
#     def pick(self):
#         try:
#             return self._items.pop()
#         except IndexError:
#             raise LookupError('pick from empty BingoCage')

#     # __call__ is also from Section 5 example - not needed to satisfy the Tombola interface but NO harm in adding extra methods
#     def __call__(self):
#         self.pick()


'''
BingoCage inherits loaded & inspect methods from Tombola

look at lotto.py
'''

# example - take a look at lotto.py

'''
in __init__: self._balls stores list(iterable) and NOT just a reference to iterable (did not assign iterable to self._balls)
    -makes our LotteryBlower FLEXIBLE because the iterable argument may be any iterable type and make sure to store its item in a LIST so we can pop items
    -good practice using list() because it makes a copy and we will be popping elements from it so we don't want the og to be changed


A Virtual Subclass of Tombola

an essential characteristic of goosetyping - ability to register a class as a VIRTUAL subclass of an ABC, even if it does NOT inherit from it
    -This is done by calling a register method on the ABC
        -Registered class then becomes a virtual subclass of the ABC and will be recognized as such by functions like issubclass and isinstance but it will NOT inherit any methods or attributes from the ABC

register method is usually invoked as a plain function but can also be used as a decorator
'''
# example - take a look at tombolist.py
# Because of the registration, the functions issubclass and isinstance act as if TomboList is a subclass of Tombola

# from Sec11_examples.tombola import Tombola
# from Sec11_examples.tombolist import TomboList

# print(issubclass(TomboList, Tombola))
# # True

# t = TomboList(range(100))
# print(isinstance(t, Tombola))
# # True

# print(TomboList.__mro__)
# # (<class 'Sec11_examples.tombolist.TomboList'>, <class 'list'>, <class 'object'>)
'''
inheritance is guided by a special class attribute named __mro__ - Method Resolution Order
    -lists the class and superclasses in the order Python uses to search for methods. 
    -if you inspect the __mro__ of TomboList, you'll see that it lists only the REAL superclasses: list and object

**Tombola is not in TomboList.__mro__ therefore TomboList does NOT inherit any methods from Tombola


How the Tombola subclasses were tested
__subclasses__() 
    -method that returns a list of the immediate subclasses of the class. The list does not include virtual subclasses

abc._get_dump(Tombola) --> returns a 4-tuple of (_abc_registry, _abc_cache, _abc_negative_cache,                            _abc_negative_cache_version)
    index the _abc_registry in abc._get_dump and build a list so we can concatenate with the result of __subclasses__()

################################# NOT IN PYTHON 3.7 #########################################
_abc_registry
    -data attribute - available ONLY in ABCs - that is bound to a WeakSet with weak references to registered virtual subclasses of the abstract class
################################# NOT IN PYTHON 3.7 #########################################
'''
# example - tombola_runner.py
# LotteryBlower     0 tests,  0 failed -OK
# TomboList         0 tests,  0 failed -OK

# take a look at the pdf for the tests that were done

'''
Usage of register in practice

in tombolist.py - we used Tombola.register as a class decorator

even if register can now be used as a decorator - it's more widely deployed as a function to register classes defined elsewhere
    example: https://hg.python.org/cpython/file/3.4/Lib/_collections_abc.py
        Sequence.register(tuple)
        Sequence.register(str)
        Sequence.register(range)
        Sequence.register(memoryview)


Geese can behave as ducks

a class can be recognized as a virtual subclass of an ABC even without registration
'''
# example - added test using issubclass
# class Struggle:
#     def __len__(self): 
#         return 23

# from collections import abc
# print(isinstance(Struggle(), abc.Sized))
# # True
# print(issubclass(Struggle, abc.Sized))
# # True

'''
dynamic subclass detection with __subclasshook__

class Struggle is considered a subclass of abc.Sized by the issubclass function because abc.Sized implements a special class method named __subclasshook__ 
    
__subclasshook__(subclass)
    (Must be defined as a class method.)

    Check whether subclass is considered a subclass of this ABC. This means that you can customize the behavior of issubclass further without the need to call register() on every class you want to consider a subclass of the ABC. (This class method is called from the __subclasscheck__() method of the ABC.)

    This method should return True, False or NotImplemented. If it returns True, the subclass is considered a subclass of this ABC. If it returns False, the subclass is not considered a subclass of this ABC, even if it would normally be one. If it returns NotImplemented, the subclass check is continued with the usual mechanism.

**Not a good idea to implement in our own ABCs if we were to make one [not worth it]
'''
# example - Sized defintion from the source code of lib/_collections.py (Python 3.4)
# class Sized(metaclass=ABCMeta):
#     __slots__ = ()

#     @abstractmethod
#     def __len__(self):
#         return 0

#     @classmethod
#     def __subclasshook__(cls, c):
#         if cls is Sized:
#             # if there is an attribute named __len__ in the __dict__ of any class listed in C.__mro__ (i.e. C and its superclasses)
#             if any("__len__" in B.__dict__ for B in C.__mro__):
#                 # return True, signaling that C is a virtual subclass of Sized
#                 return True
#         # otherwise return NotImplemented to let the subclass check proceed
#         return NotImplemented