
import model_v8 as model

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


# Doctests showing the use of field_names

for name in LineItem.field_names():
    print(name)
# description
# weight
# price

'''
No changes need in the LineItem class; field_names is inherited from model.Entity
'''

print(LineItem.mro())
# [<class '__main__.LineItem'>, <class 'model_v8.Entity'>, <class 'object'>]