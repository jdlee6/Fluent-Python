# example - class TomboList is a virtual subclass of Tombola

from random import randrange
from tombola import Tombola

# Tombolist is registered as a virtual subclass of Tombola
@Tombola.register
class TomboList(list):

    # Tombolist extends list
    def pick(self):
        # Tombolist inherits __bool__ from list and that returns True if the list is NOT empty
        if self:
            position = randrange(len(self))
            # Our pick calls self.pop, inherited from list, passing a random item index
            return self.pop(position)
        else:
            raise LookupError('pop from empty Tombolist')

    # Tombolist.load is the same as list.extend
    load = list.extend

    def loaded(self):
        # loaded delegates to bool 'footnote:[The same trick I used with 'load' doesn't work with loaded, because the list type does NOT implement __bool__, the method I'd have to bind to loaded. On the other hand, the bool built-in function doesn't need __bool__ to work, it can also use __len__]
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))

# For Python3.3 and before (can't use the .register in class decorator so you must use a standard call syntax like below)
# Tombola.register(TomboList)