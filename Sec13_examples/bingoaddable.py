# example - bingoaddable.py - AddableBingoCage extends BingoCage to support + and +=

# PEP8 recommends coding imports from the standard library ABOVE the imports of your own modules
import itertools

from Sec11_examples.tombola import Tombola
from Sec13_examples.bingocage import BingoCage

# AddableBingoCage extends BingoCage
class AddableBingoCage(BingoCage):
    def __add__(self, other):
        # Our __add__ will only work with an instance of Tombola as the second operand
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        # if that fails, raise an exception explaining what the user should do. When possible, error messages should explicitly guide the user to the solution
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            # retrieve the items from other, of it is an instance of Tombola
            other_iterable = other.inspect()
        else:
            try:
                # Otherwise, try obtain an iterator over other 
                # could use tuple(other) and it would work but at the cost of building a NEW tuple when all the .load() method needs is to iterate over its argument
                other_iterable = iter(other)
            # if that fails, raise an exception explaining what the user should do. When possible, error messages should explicitly guide the user to the solution
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        # if we got this far, we can load the other_iterable into self
        self.load(other_iterable)
        # VERY IMPORTANT: augmented assignment special methods must return self
        return self