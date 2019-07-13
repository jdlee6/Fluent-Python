# bulkfood_v4.py: Each Quantity descriptor gets a unique storage_name

class Quantity:

    # __counter is a class attribute of Quantity, counting the number of Quantity instances
    __counter = 0

    def __init__(self):
        # cls is a reference to the Quantity class
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        # the storage_name for each descriptor instance is unique because it's built from the descriptor class name and the current __counter value
        # ie. _Quantity#0
        self.storage_name = '_{}#{}'.format(prefix, index)
        # increment __counter
        cls.__counter += 1

    # we need to implement __get__ because the name of the managed attribute is NOT the same as the storage_name. 
    # look below to see what the owner argument is
    def __get__(self, instance, owner):
        # use the getattr built-in function to retrieve the value from the instance
        # instance is the managed instance (LineItem instance)
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            # use the setattr built-in to store the value in the instance
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    # now we do NOT need to pass the managed attribute name to the Quantity constructor. That was the goal for this version
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price


# testing

coconuts = LineItem('Brazilian coconut', 20, 17.05)
print((coconuts.weight, coconuts.price))
# (20, 17.05)

print((getattr(coconuts, '_Quantity#0'), getattr(coconuts, '_Quantity#1')))
# (20, 17.05)


'''
we can use the getattr and setattr built ins to store the value - instead of resorting to instance.__dict__ - because the managed attribute and the storage attribute have DIFFERENT names 
    calling getattr on the storage attribute will NOT trigger the descriptor

NOTE: __get__ receives three arguments (self, instance, owner)
    owner argument is a reference to the managed class (LineItem) and it's handy when the descriptor is used to get attributes from the class
    
    *if a managed attribute, such as weight, is retrieved via the class like LineItem.weight, the descriptor __get__ method receives None as the value for the instance argument
'''
 
# testing 

print(LineItem.weight)
#   File "bulkfood_v4.py", line 24, in __get__
#     return getattr(instance, self.storage_name)
# AttributeError: 'NoneType' object has no attribute '_Quantity#0'

'''
message should be fixed to remove 'NoneType' and '_Quantity#0'

a better message would be " 'LineItem' class has no such attribute"
'''
