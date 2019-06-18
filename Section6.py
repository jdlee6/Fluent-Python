'''
Design patterns with first-class functions

refactor Strategy using function obejcts, and discuss a similar approach to simplifying the Command pattern

Strategy is a good example of a design pattern that can be simpler in Python if you leverage functions as first class objects
    - define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it

e-commerce orders and promotional discounts example
'''

# example - Implementation Order class with pluggable discount strategies

from abc import ABC, abstractmethod
from collections import namedtuple

# Customer = namedtuple('Customer', 'name fidelity')

# class LineItem:
#     def __init__(self, product, quantity, price):
#         self.product = product
#         self.quantity = quantity
#         self.price = price

#     def total(self):
#         return self.price * self.quantity

# # the Context
# class Order:
#     def __init__(self, customer, cart, promotion=None):
#         self.customer = customer
#         self.cart = list(cart)
#         self.promotion = promotion

#     def total(self):
#         # in built-in utility function which is used to check if an object has the given named attribute and returns a Boolean
#         if not hasattr(self, '__total'):
#             self.__total = sum(item.total() for item in self.cart)
#         return self.__total

#     def due(self):
#         if self.promotion is None:
#             discount = 0
#         else:
#             discount = self.promotion.discount(self)
#         return self.total() - discount

#     def __repr__(self):
#         fmt = '<Order total: {:.2f} due: {:.2f}>'
#         return fmt.format(self.total(), self.due())

# # the Strategy: an Abstract Base Class
# class Promotion(ABC):
#     # used to declare abstract methods for properties and descriptors
#     # only affects subclasses derived using regular inheritance 
#     # when combining an abstract method with another method such as @classmethod or @staticmethod; the @abstractmethod msut be the INNERMOST decorator
#     @abstractmethod
#     def discount(self, order):
#         ''' returns discount as a positive dollar amount '''
    
# # first Concrete Strategy    
# class FidelityPromo(Promotion):
#     ''' 5% discount for customer with 1000 or more fidelity points '''

#     def discount(self, order):
#         return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# # second Concrete Strategy
# class BulkItemPromo(Promotion):
#     ''' 10% discount for each LineItem with 20 or more units '''

#     def discount(self, order):
#         discount = 0
#         for item in order.cart:
#             if item.quantity >= 20:
#                 discount += item.total() * .1
#         return discount

# # third Concrete Strategy
# class LargeOrderPromo(Promotion):
#     ''' 7% discount for orders with 10 or more distinct items '''
#     def discount(self, order):
#         distinct_items = {item.product for item in order.cart}
#         if len(distinct_items) >= 10:
#             return order.total() * .07
#         return 0


# # example - Sample usage of Order class with different promotions applied

# # 2 customers, joe (0 fidelity points) and ann (1100 fidelity points)
# joe = Customer('John Doe', 0)
# ann = Customer('Ann Smith', 1100)

# # One shopping cart with three line items
# cart = [
#     LineItem('banana', 4, .5),
#     LineItem('apple', 10, 1.5),
#     LineItem('watermelon', 5, 5.0)
# ]

# # FidelityPromo promotion gives no discount to joe
# print(Order(joe, cart, FidelityPromo()))
# # <Order total: 42.00 due: 42.00>

# # ann gets a 5% discount because she has at least 1000 points
# print(Order(ann, cart, FidelityPromo()))
# # <Order total: 42.00 due: 39.90>

# # banana_cart has 30 units of the "banana" product and 10 apples
# banana_cart = [
#     LineItem('banana', 30, .5),
#     LineItem('apple', 10, 1.5)
# ]

# # BulkItemPromo, joe gets $1.50 discount on the bananas
# print(Order(joe, banana_cart, BulkItemPromo()))
# # <Order total: 30.00 due: 28.50>

# # long_order has 10 different items at $1.00 each
# long_order = [
#     LineItem(str(item_code), 1, 1.0) for item_code in range(10)
# ]

# # joe gets a 7% discount on the whole order because of LargeOrderPromo
# print(Order(joe, long_order, LargeOrderPromo()))
# # <Order total: 10.00 due: 9.30>

# print(Order(joe, cart, LargeOrderPromo()))
# # <Order total: 42.00 due: 42.00>

###########################################################################################
'''
Function Oriented Strategy 

Look at the example above - each concrete strategy is a class with its own single method, discount therefore the 
strategy instances have no instance attributes

The example below is a refactoring of example above which replaces the concrete strategies with simple functions 
which will ultimately remve the Promo abstract class
'''

# Example - Order class with discount strategies implemented as functions

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

# the Context
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            # To compute a discount, just call the self.promotion() function
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
    
# Notice how we don't need an abstract class anymore
# Each strategy is a function
def fidelity_promo(order):
    ''' 5% discount for customers with 1000 or more fidelity points '''
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    ''' 10% discount for each LineItem with 20 or more units '''
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

def large_order_promo(order):
    ''' 7% discount for orders with 10 or more distinct items '''
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

# this example we just wrote is 12 lines shorter than the first example and using the new Order is also
# a lot more simpler

# Sample usage of Order class with promotions as functions

# same test fixtures as the example above
joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [
    LineItem('banana', 4, .5),
    LineItem('apple', 10, 1.5),
    LineItem('watermelon', 5, 5.0)
]

# To apply a discount strategy to an Order, just pass the promotion function as an argument
print(Order(joe, cart, fidelity_promo))
# <Order total: 42.00 due: 42.00>

print(Order(ann, cart, fidelity_promo))
# <Order total: 42.00 due: 39.90>

banana_cart = [
    LineItem('banana', 30, .5),
    LineItem('apple', 10, 1.5)
]

# a different promotion function is used here and in the next test
print(Order(joe, banana_cart, bulk_item_promo))
# <Order total: 30.00 due: 28.50>

long_order = [
    LineItem(str(item_code), 1, 1.0) for item_code in range(10)
]
print(Order(joe, long_order, large_order_promo))
# <Order total: 10.00 due: 9.30>

print(Order(joe, cart, large_order_promo))
# <Order total: 42.00 due: 42.00>

'''
The callouts in the example above does NOT need to instantiate a new promotion object
with each new order because the functions are ready to use 

Strategy objects often make good flyweight - a shared object that can be used in multiple contexts simulataneously
-sharing is recommended to reduce the cost of creating a new concrete strategy objects when the same strategy is applied 
over and over again with every new context - with every new Order instance, in our example
-drawback of the Strategy pattern is the runtime cost

function is more lightweight than an instance of a user defined class and there is no need for Flyweight as each
strategy function is created just once by Python when it compiles the module
-also "a shared object that can be used in multiple contexts simultaneously"
'''
