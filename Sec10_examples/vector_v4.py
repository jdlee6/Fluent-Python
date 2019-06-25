# two imports and __hash__ method added to Vector class from vector_v3.py
# example - part of vector_v2.py: __len__ and __getitem__ methods have been added to Vector class from vector_v1.py


from array import array
# imported functools to use reduce()
# imported operator to use .xor
import reprlib, math, numbers, functools, operator

class Vector:
    typecode = 'd'

    def __init__(self, components):
        # the self._components instance "protected" attribute will hold an array with the Vector components
        self._components = array(self.typecode, components)

    def __iter__(self):
        # to allow iteration, we return an iterator over self._components
        return iter(self._components)

    def __repr__(self):
        # Use reprlib.repr() to get a limited-length representation of self._components, e.g. array('d', [0.0, 1.0, 2.0, 3.0, 4.0, . . .])
        components = reprlib.repr(self._components)
        # Remove the array('d', prefix and the trailing) before plugging the string into a Vector constructor call
        # Picks out the part where it states: [0.0, ...]
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        # Build a bytes object directly from self._components
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    # No change to __eq__; good practice to keep __eq__ and __hash__ close in source code since they work together
    # for Vector instances that have thousands of components; it's very INEFFICIENT - builds two tuples copying the contents of the operands
    # def __eq__(self, other):
    #     return tuple(self) == tuple(other)

    # # alternative __eq__: using zip in a for loop for more efficient comparison
    # def __eq__(self, other):
    #     # if the len of the objects are different, they are NOT equal
    #     if len(self) != len(other):
    #         return False
    #     # zip produces a generator of tuples made from the items in each iterable argument
    #     # len comparison above is needed because zip stops producing values without warning as soon as one of the inputs is exhausted
    #     for a, b in zip(self, other):
    #         # as soon as two components are different, exit returning False
    #         if a != b:
    #             return False
    #     # Otherwise, objects are equal
    #     return True

    # Vector.__eq__ using zip and all: same logic as example above
    # all function can produce the same aggregrate computation of the for loop in one line: if all comparisons between corresponding components in the operands are True, the result is True
    # as soon as one comparison is False, all returns False
    # note how we FIRST check for the equal lengths 
    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        # Create a generator expression to lazily compute the hash of each component
        # hashes = (hash(x) for x in self._components)

        # map produces one hash for each component
        # map creates a generator that yields the results on demand and saves memory just like the method above
        hashes = map(hash, self._components)

        # Feed hashes to reduce with the xor function to compute the aggregate hash value; the third argument, 0, is the initializer
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        # We can't use hypot anymore, so we sum the squares of the components and compute the sqrt of that
        return math.sqrt(sum(x * x for x in self))
    
    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        # the only change needed from the earlier frombytes is in the last line: we pass the memoryview directly to the constructor, without unpacking with * as we did before
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        # get the class of the instance (i.e. Vector) for later use
        cls = type(self)
        # if the index argument is a slice . . .
        if isinstance(index, slice):
            # invoke the class to build another Vector instance from a slice of the _components array
            return cls(self._components[index])
        # if the index is an int or some other kind of integer . . .
        elif isinstance(index, numbers.Integral):
            # just return the specific item from _components
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            # otherwise raise an exception
            raise TypeError(msg.format(cls=cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, name):
        # Get the Vector class for later use
        cls = type(self)
        # if the name is one character, it may be one of the shortcut_names
        if len(name) == 1:
            # find position of 1-letter name; str.find would also locate 'yz' and we don't want that, this is the reason for the test above
            pos = cls.shortcut_names.find(name)
            # if the position is within range, return the array element
            if 0 <= pos < len(self._components):
                return self._components[pos]
        # if either test failed, raise AttributeError with a standard message text
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        # special handling for single character attribute names
        if len(name) == 1:
            # if name is one of xyzt, set specific error message
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            # if name is lower case, set error message about all single-letter names
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                # Otherwise, set blank error message
                error = ' '
            # If there is a non-blank error message, raise AttributeError
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        # Default case: call __setattr__ on superclass for standard behavior
        # super() function provides a way to access methods of super classes dynamically - used to delegate some task from a method in a subclass to a suitable method in a superclass
        super().__setattr__(name, value)

    