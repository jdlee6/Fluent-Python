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
# example - Partial sequence protocol implementation with __getitem__: enough for item access, iteration and the in operator
class Foo:
    def __getitem__(self, pos):
        return range(0, 30, 10)[pos]

f = Foo()
print(f[1])
# 10

for i in f:
    print(i)
# 0
# 10
# 20

print(20 in f)
# True

print(15 in f)
# False

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
# random.shuffle
from random import shuffle
l = list(range(10))
shuffle(l)
print(l)
# [5, 4, 8, 0, 1, 7, 6, 3, 2, 9]

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
from random import shuffle

deck = FrenchDeck()

# create a function that takes deck, position, and card as arguments
def set_card(deck, position, card):
    deck._cards[position] = card

# assign that function to an attribute named __setitem__ in the FrenchDeck class
FrenchDeck.__setitem__ = set_card
# deck can now be sorted because FrenchDeck now implements the necessary method of the MUTABLE sequence protocol
shuffle(deck)
print(deck[:5])
# [Card(rank='K', suit='diamonds'), Card(rank='3', suit='diamonds'), Card(rank='9', suit='hearts'), Card(rank='Q', suit='diamonds'), Card(rank='2', suit='clubs')]

'''
set_card knows that the deck object has an attribute named _cards and _cards MUST be a mutable sequence
set_card function is then attached to the FrenchDeck class as the __setitem__ special method
    example of monkey patching: changing a class or module at run time without touching the source code
'''
