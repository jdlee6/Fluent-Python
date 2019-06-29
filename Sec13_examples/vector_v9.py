# vector_v6.py; added unary operators (- +) support

from array import array
import reprlib, math, numbers, functools, operator, itertools
# import the numbers module for type checking
import numbers

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

    # def __eq__(self, other):
    #     return len(self) == len(other) and 
    #                all(a == b for a, b in zip(self, other))

    def __eq__(self, other):
        # if the other operand is an instance of Vector (or of a Vector subclass), perform the comparison as before
        if isinstance(other, Vector):
            return (len(self) == len(other) and
                         all(a == b for a, b in zip(self, other)))
        else:
            # otherwise, return NotImplemented
            return NotImplemented

    def __hash__(self):
        hashes = map(hash, self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __neg__(self):
        # to compute -v, build a new Vector with every component of self negated
        return Vector(-x for x in self)

    def __pos__(self):
        # to computer +x, buid a new Vector with every component of self
        return Vector(self)

    # put in a try and except block; safely overloaded the + operator by writing __add__ and __radd__
    def __add__(self, other):
        try: 
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented
    
    def __radd__(self, other):
        return self + other

    # use isinstance() to check the type of the scalar BUT we don't hard code it; instead we check against numbers.Real ABC
    def __mul__(self, scalar):
        # if scalar is an instance of a numbers.Real subclass, create new Vector with multiplied component values
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        # Otherwise, raise TypeError with an explicit message
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        # In this example, __rmul__ works fine by just performing self * scalar method, delegating to the __mul__ method
        return self * scalar

    # @ operator // __matmul__ // matrix multiplication
    def __matmul__(self, other):
        try:
            return sum(a*b for a,b in zip(self, other))
        except TypeError:
            return NotImplemented
        
    def __rmatmul__(self, other):
        return self @ other

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

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))
