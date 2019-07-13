# model_v4c.py: this is where the Quantity descriptor class now resides

# bulkfood_v4b.py (partial listing): when invoked through the managed class, __get__ returns a reference to the descriptor itself

class Quantity:

    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)

    def __get__(self, instance, owner):
        if instance is None:
            # if the call was NOT through an instance, return the descriptor itself
            return self
        else:
            # otherwise, return the managed attribute value, as usual
            return getattr(instance, self.storage_name)
    
    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')

