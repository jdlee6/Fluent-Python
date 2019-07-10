# explore0.py: turn a JSON dataset into a FrozenJSON holding nested FrozenJSON objects, lists and simple types

from collections import abc

class FrozenJSON:
    '''
    a read only facade for navigating a JSON like object using attribute notation
    '''

    def __init__(self, mapping):
        # build a dict from the mapping argument. This serves two purposes: ensures we got a dict (or something that can be converted to one) and makes a copy for safety
        self.__data = dict(mapping)

    # __getattr__ is called only when there's no attribute with that name
    def __getattr__(self, name):
        if hasattr(self.__data, name):
            # if name matches an attribute of the instance__data, return that. This is how calls to methods like keys are handled
            return getattr(self.__data, name)
        else:
            # otherwise, fetch the item with key name from self.__data and return the result of calling FrozenJSON.build() on that
            # a KeyError exception may occur in the expression self.__data[name]. It should be handled and an AttributeError raised instead, since that's what is expected from __getattr__
            return FrozenJSON.build(self.__data[name])
    
    @classmethod
    # this is alternate constructor, a common use for the @classmethod
    def build(cls, obj):
        # if obj is a mapping, build a FrozenJSON with it
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        # if it is a MutableSequence, it MUST be a list, so we build a list by passing every item in obj recursively to .build()
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        # if it is NOT a dict or list, return the item as it is
        else:
            return obj


'''
FrozenJSON class has only TWO methods (__init__ and __getattr__) along with a __data instance attribute
    1. checks if self.__data dict has an attr by that name (NOT a key)
    2. handles the dict methods and if self.__data does NOT have an attribute with the given name
    3. __getattr__ uses the name as a key to retrieve an item from self.__dict and passes that item to FrozenJSON.build()

the keystone of the FrozenJSON class is the __getattr__ method
    ONLY invoked by the interpreter when the usual process fails to retrieve an attribute
        ie. when the named attribute CANNOT be found in the instance NOR in the class or in its superclasses

*the last test in explore_doctest.py presents a minor issue with the implementation because it returns a KeyError

nested data structures are CONVERTED into FrozenJSON
'''