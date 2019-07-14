# model_v6.py: a class decorator (def entity(cls):)

# Decorator gets class as argument
def entity(cls):
    # iterate over dict holding the class attributes
    for key, attr in cls.__dict__.items():
        # if the attribute is one of our Validated descriptors...
        if isinstance(attr, Validated):
            # NOTE: type is a class which is why we can do type(attr).__name__
            type_name = type(attr).__name__
            # ...set the storage_name to use the descriptor class name and the managed attribute name, e.g. _NonBlank#description
            attr.storage_name = '_{}#{}'.format(type_name, key)
    # return the modified class
    return cls


''' the rest of the code is identical to model_v5.py from Section20 '''


import abc

class AutoStorage:

    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
    

class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        '''return validated value or raise ValueError'''


class Quantity(Validated):
    '''a number greater than zero'''

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

    
class NonBlank(Validated):
    '''a string with at least one non-space character'''

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value