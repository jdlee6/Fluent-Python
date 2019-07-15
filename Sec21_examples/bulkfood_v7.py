# bulkfood_v7.py: Inheriting from model.Entity can work, if a metaclass is behind the scene

import Sec21_examples.model_v7 as model

# LineItem is a subclass of model.Entity
class LineItem(model.Entity):
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price