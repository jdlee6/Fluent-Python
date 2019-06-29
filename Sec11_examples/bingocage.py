from Sec11_examples.tombola import Tombola
import random

# BingoCage class explicitly extends Tombola
class BingoCage(Tombola):
    def __init__(self, items):
        # Pretend we'll use this for online gaming. random.SystemRandom implements the random API on top of the os.urandom(...) function which provides random bytes "suitable for cryptographic"
        # SystemRandom class uses the system function os.urandom() to generate random numbers from sources provided
        self._randomizer = random.SystemRandom()
        self._items = []
        # Delegate the initial loading to the .load() method
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        # Instead of the plain random.shuffle() function, we use the .shuffle() method of our SystemRandom instance
        self._randomizer.shuffle(self._items)

    # pick is implemented as in Section 5 example
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    # __call__ is also from Section 5 example - not needed to satisfy the Tombola interface but NO harm in adding extra methods
    def __call__(self):
        self.pick()

