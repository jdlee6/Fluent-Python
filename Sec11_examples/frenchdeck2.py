# frenchdeck2.py - FrenchDeck2, a subclass of collections.MutableSequence

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range (2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                                         for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    # __setitem__ is all we need to enable shuffling
    def __setitem__(self, position, value):
        self._cards[position] = value

    # subclassing MutableSequence forces us to implement __delitem__, an abstract method of that ABC
    # if not: TypeError: Can't instantiate abstract class HostList with abstract methods __delitem__
    def __delitem__(self, position):
        del self._cards[position]

    # we are also required to implement insert, the third abstract method of MutableSequence
    # if not: TypeError: Can't instantiate abstract class FrenchDeck2 with abstract methods insert
    def insert(self, position, value):
        self._cards.insert(position, value)