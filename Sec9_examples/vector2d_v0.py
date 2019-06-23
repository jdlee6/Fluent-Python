# example - class Vector2d

from array import array
import math

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        # use exactly two leading underscores (with zero or one trailing underscore) to make an attribute private
        self.__x = float(x)
        self.__y = float(y)

    # the @property decorator marks the getter method of property
    @property
    # the getter method is named after the public property it exposes: x
    def x(self):
        # just return self.x
        return self.__x

    # repeat same formula for y property
    @property
    def y(self):
        return self.__y

    def __iter__(self):
        # every method that just reads the x, y components can stay as they were, reading the public properties via self.x and self.y instead of the private attribute, so this listing omits the rest of the code for the class
        return (i for i in (self.x, self.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        class_name = type(self).__name__
        # __repr__ builds a string by interpolating the components with {!r} to get their repr; because Vector2d is iterable, *self feeds the x and y components to format
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        # from an iterable Vector2d it's easy to build a tuple for display as an ordered pair
        return str(tuple(self))

    def __bytes__(self):
        # to generate bytes, we convert the typecode to bytes and concatenate . . .
        # ... bytes converted from an array built by iterating over the instance
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        # to quickly compare all components, build tuples out of the operands. this works for operands that are instances of Vector2d, but has issues
        return tuple(self) == tuple(other)

    def __abs__(self):
        # the magnitude is the length of the hypotenuse of the triangle formed by x and y components
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # __bool__ uses abs(self) to compute the magnitude, then converts it to bool, so 0.0 becomes False, non-zero is True
        return bool(abs(self)) 

    # build def angle(self)
    # angle method using math.atan2() function - returns the value of atan(y/x) in radians. returns a numeric value between -\pi and pi representing the angle, theta, of a (x, y) point and positive x-axis
    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        # Format ends with 'p': use polar coordinates
        if fmt_spec.endswith('p'):
            # remove 'p' suffix from fmt_spec
            fmt_spec = fmt_spec[:-1]
            # build tuple of polar coordinates: (magnitude, angle)
            coords = (abs(self), self.angle())
            # configure outer format with angle brackets
            outer_fmt = '<{}, {}>'
        else:
            # otherwise, use x, y components of self for rectangular coordinates
            coords = self
            # configure outer format with parenthesis
            outer_fmt = '({}, {})'

        # # use the format built-in to apply the fmt_spec to each vector component, building an iterable of formatted strings

        # generate iterable with components as formatted strings
        components = (format(c, fmt_spec) for c in coords)
        # plug the formatted strings in the formula '(x, y)'
        return '({}, {})'.format(*components)

    @classmethod
    # No self argument; class method so it requires the cls as a passed in parameter
    def frombytes(cls, octets):
        # read the type code from the FIRST byte
        # chr() returns a string representing a character whose Unicode code point is an integer 
            # example: chr(8364) --> '€'
        typecode = chr(octets[0])
        # Create a memoryview from the octets binary sequence and use the typecode to cast it
        # memoryview.cast method lets you change the way multiple bytes are read or written as units without moving bits around
        memv = memoryview(octets[1:]).cast(typecode)
        # unpack the memoryview resulting from the cast into the pair of arguments needed for the constructor
        return cls(*memv)