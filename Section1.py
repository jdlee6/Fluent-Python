# Chapter 1 Python Data Model

# special method names are always spelled with leading and trailing double underscores
# these methods are also known as magic and dunder methods
# for example: obj[key] would be the same as obj.__getitem__(key)


''' A Pythonic Card Deck '''
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

# namedtuple( ) can be used to build classes of objects that just bundles of attributes with no custom methods

# beer_card = Card('7', 'diamonds')
# print(beer_card)
# output: Card(rank='7', suit='diamonds')

# this is what the __len__ method provides
deck = FrenchDeck()
# print(len(deck))
# output: 52

# this is what the __getitem__ method provides
# print(deck[0])
# print(deck[-1])
#output: Card(rank='2', suit='spades')
#output: Card(rank='A', suit='hearts')

# Python has a function to get a random item (random.choice)
# from random import choice
# print(choice(deck))

'''
1. The users of your classes don't have to memorize method names (can simply just make your own)
2. No need to reinvent the wheel when you have the random module 
'''

# note that the __getitem__ delegates to the [] operator of self.cards which means our deck automatically supports slicing
# top three cards of a brand new deck
# print(deck[:3]) 
# picking just the aces by starting on index 12 and skipping 13 cards at a time
# print(deck[12::13])

# the __getitem__ method also makes our deck iterable:
# for card in deck:
#     print(card)

# reversing the iteration
# for card in reversed(deck):
#     print(card)


# if a collection has no __contains__ method, the in operator does a sequential scan
# this method works because our FrenchDeck class is iterable
# print(Card('Q', 'hearts') in deck)
# print(Card('7', 'beasts') in deck)


# what about sorting? this is a function that ranks cards by spades (highest), then hearts, diamonds, and clubs
# this will return 0 for the 2 of clubs and 51 for the ace of spaces:

# suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

# def spades_high(card):
#     rank_value = FrenchDeck.ranks.index(card.rank)
#     return rank_value * len(suit_values) + suit_values[card.suit]

# for card in sorted(deck, key=spades_high):
#     print(card)

''' Because we implemented the special methods __len__ and __getitem__, the French Deck behaves like a standard Python sequence, allowing it to benefit from core language features - like iteration and slicing - and also with random.choice, reversed, and sorted '''

# How about shuffling? it cannot be shuffled because we made it immutable (tuple)

''' Typically the user does NOT need to call dunder methods other than specfiying them for the Python interpreter.
The only special method that is frequently called by user code DIRECTLY is __init__ which is to invoke the initializer of the superclass '''
####################################################################################################

# Emulating numeric types

# There are several special methods that allow user objects to respond to operators such as +
''' Vector Class example '''

from math import hypot

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'
    
    def __abs__(self):
        return hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

# v1 = Vector(2, 4)
# v2 = Vector(2 ,1)
# print(v1 + v2)
# output: Vector(5, 5)

# v = Vector(3, 4)
# print(abs(v))
# print(v * 3)
# print(abs(v * 3))
# 5.0
# Vector(9, 12)
# 15.0

''' Note how none of the four special methods are directly called within the class '''

####################################################################################################

# String Representation
''' if we didn't implement this dunder method in our Vector class example then we would probably returned something like this: <Vector object at 0x10e100070> '''
# __repr__ --> returns a string in a format that is designed
# __str__ --> returns a string when it is called by the str( ) constructor

# choose __repr__ over __str__ when selecting one over the other

# Arithmetic operators
# + and * --> show basic usage of __add__ and __mul__ 

# Boolean value
# bool( ) returns False if the magnitude of the vector is zero and True otherwise

####################################################################################################

''' Overview of special methods (refer to Table 1-1 and Table 1-2) '''

