# bulkfood_v2b.py: same as bulkfood_v2.py but WITHOUT using decorators

class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    # a plain getter
    def get_weight(self):
        return self.__weight

    # a plain setter
    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    # build the property and assign it to a public class attribute
    weight = property(get_weight, set_weight)    