# bulkfood_v3.py: Quantity descriptors MANAGE attributes in LineItem

# Descriptor is a protocol based feature; NO subclassing is needed to implement one
class Quantity:

    def __init__(self, storage_name):
        # each Quantity instance will have a storage_name attribute: that's the name of the attribute which will hold the value in the managed instances
        self.storage_name = storage_name

    # __set__ is called when there is an attempt to assign to the managed attribute. Here self is the descriptor instance (ie. LineItem.weight or LineItem.price)
    # instance is the managed instance (a LineItem instance), and value is the value being assigned
    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:
    # the first descriptor instance is bound to the weight attribute
    weight = Quantity('weight')
    # the second descriptor instance is bound to the price attribute
    price = Quantity('price')

    # the rest of the class body is as simple and clean as the original code in bulkfood_v1.py from Section19
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# testing - prevents the sales of truffles for $0

truffle = LineItem('White truffle', 100, 0)
# ValueError: value must be > 0