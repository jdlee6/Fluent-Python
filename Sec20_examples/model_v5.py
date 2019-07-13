# model_v5.py: The refactored descriptor classes

import abc

# AutoStorage provides most of the functionality of the former Quantity descriptor ...
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
        # ... except validation
        setattr(instance, self.storage_name, value)
    

# Validated is abstract but also inherits from AutoStorage
class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        # __set__ delegates validation to a validate method ...
        value = self.validate(instance, value)
        # ... then uses the returned value to invoke __set__ on a superclass, which performs the actual storage
        super().__set__(instance, value)

    @abc.abstractmethod
    # in this class, validate is an abstract method
    def validate(self, instance, value):
        '''return validated value or raise ValueError'''


# Quantity and NonBlank inherit from Validated
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
        # requiring the concrete validate methods to return the validated value gives them an opportunity to clean up, convert or normalize the data received. In this case, the value is returned stripped of leading and trailing blanks
        return value


'''
use Quantity and NonBlank to automate the validation of instance attributes
'''
