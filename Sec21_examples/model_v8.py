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


# model_v8.py: the EntityMeta metaclass uses __prepare__ and Entity now has a field_names class method

import collections

class EntityMeta(type):
    '''Metaclass for business entities with validated fields'''

    @classmethod
    def __prepare__(cls, name, bases):
        # return an empty OrderedDict instance, where the class attributes will be stored
        return collections.OrderedDict()

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        # create a _field_names attribute in the class under construction
        cls._field_names = []
        # this line is unchanged from the previous version, but attr_dict here is the OrderedDict obtained by the interpreter when it called __prepare__ before calling __init__. Therefore, this for loop will go over the attributes in the ORDER they were added
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)
                # add the name of each Validated field found to _field_names
                cls._field_names.append(key)
            

class Entity(metaclass=EntityMeta):
    '''Business entity with validated fields'''

    @classmethod
    # the field_names class method simply yields the names of the fields in the order they were added
    def field_names(cls):
        for name in cls._field_names:
            yield name



