# bulkfood_v6.py: LineItem using Quantity and NonBlank descriptors

import model_v6 as model

# the only change in this class is the added decorator
@model.entity
class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price


# bulkfood_v6.py: doctests for new storage_name descriptor attitudes

raisins = LineItem('Golden raisins', 10, 6.95)
print(dir(raisins)[:3])
# ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']

print(LineItem.description.storage_name)
# _NonBlank#description

print(raisins.description)
# Golden raisins

print(getattr(raisins, '_NonBlank#description'))
# Golden raisins