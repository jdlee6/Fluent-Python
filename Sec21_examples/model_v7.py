# model_v7.py: the EntityMeta metaclass and one instance of it, Entity

class EntityMeta(type):
    '''Metaclass for business entities with validated fields'''

    def __init__(cls, name, bases, attr_dict):
        # Call __init__ on the superclass (type in this case)
        super().__init__(name, bases, attr_dict)
        # Same logic as the @entity decorator in model_v6.py
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)

# this class exists for convenience ONLY: the user of this module can just subclass Entity and NOT worry about EntityMeta - or even be aware of its existence
class Entity(metaclass=EntityMeta):
    '''Business entity with validated fields'''


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