# example - part of vector_v2.py: __len__ and __getitem__ methods have been added to Vector class from vector_v1.py


from array import array
import reprlib, math, numbers

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

    def __eq__(self, other):
        return tuple(self) == tuple(other)

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