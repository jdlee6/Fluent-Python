# bulkfood_v2prop.py: quantity property factory

# the storage_name argument determines where the data for each property is stored; for the weight, the storage name will be "weight"
def quantity(storage_name):

    # the first argument of the qty_getter could be named "self", but that would be strange since this is NOT a class body; instance refers to the LineItem INSTANCE where the attribute will be stored
    def qty_getter(instance):
        # qty_getter references storage_name, so it will be preserved in the closure of this function; the value is retrieved directly from the instance.__dict__ to BYPASS the property and avoid an infinite recursion
        return instance.__dict__[storage_name]

    # qty_setter is defined, also taking instance as first argument
    def qty_setter(instance, value):
        if value > 0:
            # the value is stored directly in the instance.__dict__, again BYPASSING the property
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')
    
    # build a custom property object and return it
    return property(qty_getter, qty_setter)


'''
remember that a CLOSURE occurs when a function has access to a local variable from an enclosing scope that has finished its execution
'''


# bulkfood_v2prop.py (part 2): the quantity property factory in class object LineItem

class LineItem:
    # use the factory to define the first custom property, weight, as a class attribute
    weight = quantity('weight')
    # this second call builds another custom property, price
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        # here the property is ALREADY active, making sure a negative or 0 weight is rejected
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        # the properties are also in use here, retrieving the values stored in the instance
        return self.weight * self.price
    
'''
remember that properties are class attributes

when building each quantity property, we need to pass the name of the LineItem attribute that will be managed by that specific property

ie. weight = quantity('weight')
'''


# testing: the quantity property factory

nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
# reading the weight and price through the properties shadowing the namesake instance attributes
print(nutmeg.weight, nutmeg.price)
# 8 13.95

# using vars to inspect the nutmeg instance: here we see the actual instance attributes used to stored the values
print(sorted(vars(nutmeg).items()))
# [('description', 'Moluccan nutmeg'), ('price', 13.95), ('weight', 8)]