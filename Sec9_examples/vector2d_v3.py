# example - make class vector2d object an immutable class object

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

# remaining methods follow (ommitted in book listing)
