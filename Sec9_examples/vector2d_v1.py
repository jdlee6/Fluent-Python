# example - the snippet below shows only the frombytes class method which is added to the Vector2d definition in vector2d_v0.py

# Class method is modified by the class method decorator
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