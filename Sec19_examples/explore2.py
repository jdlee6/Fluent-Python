# explore2.py: using __new__ instead of build to construct new object that may or may NOT be instances of FrozenJSON

from collections import abc
import keyword

class FrozenJSON:
    ''' A read only facade for navigating a JSON-like object using attribute notation '''

    # as a class method, the FIRST argument __new__ gets is the class itself, and the remaining arguments are the same that __init__ gets, except for self
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            # the default behavior is to delegate to the __new__ of a super class. In this case, we are calling __new__ from the object base class, passing FrozenJSON as the only argument
            return super().__new__(cls)
        # the remaining lines of __new__ are exactly as in the old build method
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
                self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            # This was where FrozenJSON.build was called before; now we just call the FrozenJSON constructor
            return FrozenJSON(self.__data[name])


'''
the __new__ method gets the class as the first argument because the created object will be an instance of that class

when the expression super().__new__(cls) effectively calls object.__new__(FrozenJSON), the instance built by the object class is actually an instance of FrozenJSON
    ie. __class__ attribute of the new instance will hold a reference to FrozenJSON
'''
