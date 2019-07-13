# bulkfood_v4c.py: LineItem definition uncluttered and importing Quantity descriptor class from model_v4c.py

# import the model_v4c module, giving it a friendlier name
import model_v4c as model

class LineItem:
    # put model.Quantity to use
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# testing

print(LineItem.price)
# <model_v4c.Quantity object at 0x7fba54eeab00>

br_nuts = LineItem('Brazil nuts', 10, 34.95)
print(br_nuts.price)
# 34.95