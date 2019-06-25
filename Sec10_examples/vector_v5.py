# vector_v5.py; doctests and all code for final Vector class. Callouts highlight additions needed to support __format__

from array import array
# import itertools to use chain function in __format__
import reprlib, math, numbers, functools, operator, itertools

class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
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

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = map(hash, self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    
    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ' '
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    # compute one of the angular coordinates, using math formulas adapted from the n-sphere article
    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    # create a generator expression to compute all angular coordinates on demand
    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        # hyperspherical coordinates
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            # user itertools.chain to produce generator expressions to iterate seamlessly over the magnitude and the angular coordinates
            # itertools.chain makes an iterator that returns elements from the first iteral until it is exhausted, then next iterable until exhausted, until all of the iterables are exhausted
            coords = itertools.chain([abs(self)], self.angles())
            # configure spherical coordinate display with angular brackets
            outer_fmt = '<{}>'
        else:
            coords = self
            # configure cartesian coordinate display with parenthesis
            outer_fmt = '({})'
        # Create generator expression to format each coordinate item on demand
        components = (format(c, fmt_spec) for c in coords)
        # plug formatted components separated by commas inside brackets or parenthesis
        return outer_fmt.format(', '.join(components))