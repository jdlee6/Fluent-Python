# example - LotteryBlower is a concrete subclass that overrides the inspect and loaded methods from Tombola

import random

from tombola import Tombola

class LotteryBlower(Tombola):
    def __init__(self, iterable):
        # initializer accepts any iterable: the argument is used to build a list
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            # The random.randrange() function raises ValueError if the range is empty, so we catch that and throw LookupError instead, to be compatible with Tombola
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty BingoCage')
        # Otherwise the randomly selected item is popped from self._balls
        return self._balls.pop(position)

    # Override loaded to avoid calling inspect (as Tombola.loaded does in the previous example). We can make it faster by working with self._balls directly - no need to build a whole sorted tuple
    def loaded(self):
        return bool(self._balls)

    # Override inspect with one-liner
    def inspect(self):
        return tuple(sorted(self._balls))
