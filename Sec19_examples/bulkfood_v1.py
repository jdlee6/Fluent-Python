# bulkfood_v1.py: the simplest LineItem class

class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# problems: negative weight results in a negative subtotal

raisins = LineItem('Golden raisins', 10, 6.95)
print(raisins.subtotal())
# 69.5

# garbage in
raisins.weight = -20

# garbage out
print(raisins.subtotal())
# -139.0