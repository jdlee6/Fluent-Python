# bulkfood_v5.py: LineItem using Quantity and NonBlank descriptors

# import the model_v5 module and give it a friendlier name
import model_v5 as model

class LineItem:
    # put model.NonBlank to use. The rest of the code is unchanged
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    