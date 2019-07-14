from record_factory import record_factory

# Factory signature is similar to that of namedtuple: class name, followed by attribute names in a SINGLE string, separated by spaces or commas
Dog = record_factory('Dog', 'name weight owner')
rex = Dog('Rex', 30, 'Bob')

# nice repr
print(rex)
# Dog(name='Rex', weight=30, owner='Bob')

# Instances are iterable, so they can be conveniently unpacked on assignment
name, weight, _ = rex
print((name, weight))
# ('Rex', 30)

# ... or when passing to functions like format
print("{2}'s dog weighs {1} kg".format(*rex))
# Bob's dog weighs 30 kg

# A record instance is mutable
rex.weight = 32
print(rex)
# Dog(name='Rex', weight=32, owner='Bob')

# the newly created class inherits from object - NO relationship to our factory
print(Dog.__mro__)
# (<class 'record_factory.Dog'>, <class 'object'>)

