# example - Vector2d instances have several representations

from vector2d_v0 import Vector2d

v1 = Vector2d(3, 4)
# The components of a Vector2d can be accessed directly as attributes (no getter method calls)
print(v1.x, v1.y)
# 3.0 4.0

x, y = v1
# A Vector2d can be unpacked to a tuple of variables
print((x, y))
# (3.0, 4.0)

# The repr of a Vector2d emulates the source code for constructing the instance when you call print(repr(. . .))
print(repr(v1))
# Vector2d(3.0, 4.0)

# Using eval here shows that the repr of a Vector2d is a faithful representation of its constructor call
v1_clone = eval(repr(v1))
print(v1_clone)
# (3.0, 4.0)

# Vector2d supports comparison with ==; this is useful for testing
print(v1 == v1_clone)
# True

# print calls str, which for Vector2d produces an ordered pair display
print(v1)
# (3.0, 4.0)

# bytes uses the __bytes__ method to produce a binary representation
octets = bytes(v1)
print(octets)
# b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'

# abs uses the __abs__ method to return the magnitude of the Vector2d
print(abs(v1))
# 5.0

# bool uses the __bool__ method to return False for a Vector2d of zero magnitude or True otherwise
print((bool(v1), bool(Vector2d(0, 0))))
# (True, False)