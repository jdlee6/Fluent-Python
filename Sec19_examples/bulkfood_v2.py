# bulkfood_v2.py: a LineItem with a weight property

class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        # here the property setter is ALREADY in use, making sure that NO instances with negative weight can be created
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price

    # @property decorates the getter method
    @property
    # the methods that implement a property all have the name of the PUBLIC attribute: weight
    def weight(self):
        # The actual value is stored in a private attribute __weight
        # the __ prefix PREVENTS access to attribute except through accessors in this case (weight)
        # f.weight instead of f.__weight
        return self.__weight

    # the decorated getter has a .setter attribute, which is also a decorator; this ties the getter and setter together
    @weight.setter
    def weight(self, value):
        if value > 0:
            # if the value is greater, we set the PRIVATE __weight
            self.__weight = value
        else:
            # Otherwise, ValueError is raised
            raise ValueError('value must be > 0')


# Testing
walnuts = LineItem('walnuts', 1, 10.00)
print(walnuts.weight)
# 1

# Remember that we CAN NOT access private attributes like __weight INSTEAD we have to call it through its accessor
# print(walnuts.__weight)
# # AttributeError: 'LineItem' object has no attribute '__weight'

# the weight of watermelon is set to 0
watermelon = LineItem('watermelon', 0, 10.00)

# a ValueError is now outputted because the weight is NOT greater than 0
print(watermelon.weight)
# ValueError: value must be > 0