# method_is_descriptor.py: a Text class, derived from UserString

import collections

class Text(collections.UserString):

    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]


# experiments with a method
word = Text('forward')

# the repr of a Text instance looks like a Text constructor call that would make an equal instance
print(word)
# forward

# the reverse method returns the text spelled backwards
print(word.reverse())
# drawrof

# a method called on the class works as a function
print(Text.reverse(Text('backward')))
# drawkcab

# Note the different types: a function and a method
print(type(Text.reverse), type(word.reverse))
# <class 'function'> <class 'method'>

# Text.reverse operates as a function, even working with objects that are NOT instances of Text
print(list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')])))
# ['diaper', (30, 20, 10), Text('desserts')]

# Any function is a non-overriding descriptor. Calling its __get__ with an instance retrieves a method bound to that instance
print(Text.reverse.__get__(word))
# <bound method Text.reverse of Text('forward')>

# calling the function's __get__ with None as the instance argument retrieves the function itself
print(Text.reverse.__get__(None, Text))
# <function Text.reverse at 0x7f5c91b5b510>

# the expression word.reverse actually invokes Text.reverse.__get__(word), returning the bound method
print(word.reverse)
# <bound method Text.reverse of Text('forward')>

# the bound method object has a __self__ attribute holding a reference to the instance on which the method was called
print(repr(word.reverse.__self__))
# Text('forward')

# the __func__ attribute of the bound method is a reference to the original function attached to the managed class
print(word.reverse.__func__ is Text.reverse)
# True