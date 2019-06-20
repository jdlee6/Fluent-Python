'''
Design patterns with first-class functions

refactor Strategy using function objects, and discuss a similar approach to simplifying the Command pattern

Strategy is a good example of a design pattern that can be simpler in Python if you leverage functions as first class objects
    - define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it

e-commerce orders and promotional discounts example
'''

# example - Implementation Order class with pluggable discount strategies

# from abc import ABC, abstractmethod
# from collections import namedtuple

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
# def fidelity_promo(order):
#     ''' 5% discount for customers with 1000 or more fidelity points '''
#     return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# def bulk_item_promo(order):
#     ''' 10% discount for each LineItem with 20 or more units '''
#     discount = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount += item.total() * .1
#     return discount

# def large_order_promo(order):
#     ''' 7% discount for orders with 10 or more distinct items '''
#     distinct_items = {item.product for item in order.cart}
#     if len(distinct_items) >= 10:
#         return order.total() * .07
#     return 0

# this example we just wrote is 12 lines shorter than the first example and using the new Order is also
# a lot more simpler

# Sample usage of Order class with promotions as functions

# # same test fixtures as the example above
# joe = Customer('John Doe', 0)
# ann = Customer('Ann Smith', 1100)
# cart = [
#     LineItem('banana', 4, .5),
#     LineItem('apple', 10, 1.5),
#     LineItem('watermelon', 5, 5.0)
# ]

# # To apply a discount strategy to an Order, just pass the promotion function as an argument
# print(Order(joe, cart, fidelity_promo))
# # <Order total: 42.00 due: 42.00>

# print(Order(ann, cart, fidelity_promo))
# # <Order total: 42.00 due: 39.90>

# banana_cart = [
#     LineItem('banana', 30, .5),
#     LineItem('apple', 10, 1.5)
# ]

# # a different promotion function is used here and in the next test
# print(Order(joe, banana_cart, bulk_item_promo))
# # <Order total: 30.00 due: 28.50>

# long_order = [
#     LineItem(str(item_code), 1, 1.0) for item_code in range(10)
# ]
# print(Order(joe, long_order, large_order_promo))
# # <Order total: 10.00 due: 9.30>

# print(Order(joe, cart, large_order_promo))
# # <Order total: 42.00 due: 42.00>

'''
The callouts in the example above does NOT need to instantiate a new promotion object
with each new order because the functions are ready to use 

Strategy objects often make good flyweights - a shared object that can be used in multiple contexts simulataneously
-sharing is recommended to reduce the cost of creating a new concrete strategy objects when the same strategy is applied 
over and over again with every new context - with every new Order instance, in our example
-drawback of the Strategy pattern is the runtime cost

function is more lightweight than an instance of a user defined class and there is no need for Flyweight as each
strategy function is created just once by Python when it compiles the module
-also "a shared object that can be used in multiple contexts simultaneously"

Let's say you want to create a "meta-strategy" that selects the best available discount for a given Order

Choosing the best strategy: a simple approach
'''
# once you get used to the idea that functions are first class objects - you can understand that you can hold functions in data structures

# example - the best_promo function applies all discounts and returns the largest (best_promo finds the maximum discount iterating over a list of functions)

# # promos: list of the strategies implemented as functions
# promos = [
#     fidelity_promo,
#     bulk_item_promo,
#     large_order_promo,
# ]

# # best_promo takes an instance of Order as argument, as do the other *_promo functions
# def best_promo(order):
#     ''' Select best discount available '''
#     # using a generator expression, we apply each of the functions from promos to the order and return the maximum discount computed
#     return max(promo(order) for promo in promos)

# # best_promo selected the larger_order_promo for customer joe
# print(Order(joe, long_order, best_promo))
# # <Order total: 10.00 due: 9.30>

# # here joe got the discount from bulk_item_promo for ordering lots of bananas
# print(Order(joe, banana_cart, best_promo))
# # <Order total: 30.00 due: 28.50>

# # checking out with a simple cart, best_promo gave loyal customer ann the discount for the fidelity_promo
# print(Order(ann, cart, best_promo))
# # <Order total: 42.00 due: 39.90>

# this method works fine; but a simple bug is that you may want to add a new strategy and you might forget to add it to the promos list


###########################################################################################


# Finding strategies in a module

'''
similar to functions; modules are also first class objects and the Standard Library provides several functions to handle them
- globals(): returns a dictionary representing the current global symbol table. ALWAYS the dictionary of a current module
'''

# example - the promos list is built by introspection of the module global() namespace

# # iterate over each name in the dictionary returned by globals()
# promos = [
#     globals()[name] for name in globals()
#     # select only names that end with the _promo suffix
#     if name.endswith('promo')
#     # filter out best_promo itself, to avoid an infinite recursion
#     and name != 'best_promo'
# ]

# def best_promo(order):
#     ''' Select best discount available '''
#     # no changes were made inside best_promo
#     return max(promo(order) for promo in promos)

'''
Another way of collecting the available promotions would be to create a module and put all strategy functions there EXCEPT 
for best_promo

list of strategy functions below is built by introspectioon of a separate module called promotions
depends on importing the promos module as well as inspect (provides high level introspection functions)

The example below shows one possible use of module introspection
'''

# example - promos list is buily by introspection of a new promos module

import promos, inspect

# getmembers return all the members of an object in a list of name of (name, value) pairs sorted by name
# (object[, parameters]) - if optional parameter is supplied, only members that match that argument is supplied
promos = [
    func for name, func in inspect.getmembers(promos, inspect.isfunction)
]

print(promos)
# [<function bulk_item_promo at 0x7f73ebc17048>, <function fidelity_promo at 0x7f73ebbf4f28>, <function large_order_promo at 0x7f73ebc170d0>]

def best_promo(order):
    ''' Select best discount available '''
    return max(promo(order) for promo in promos)

'''
A more explicit alternative for dynamically collecting promotional discount functions would be to use a simple decorator '''

###########################################################################################

'''
Command - another design pattern that can be simplified by the use of functions passed as arguments

goal of Command is to decouple an object that invokes an operation (Invoker) from the provider object that implements it(Receiver)
    -each invoker is a menu item in a graphical application and the receivers are the document being edited or the application itself

    -idea is to put a Command object between the two, implementing an interface with a single method, execut which alls some method in the Receiver to perform the desired operation

Python provides a couple of alternatives, to support undo, which may require more than a simple callback function
    -callable instance like MacroCommand, below, can keep whatever state is necessary and provide extra methods in addition to __call__
    -closure can be used to hold the internal state of a function between calls
'''

# example - each instance of MacroCommand has an internal list of commands
class MacroCommand:
    ''' A command that executes a list of commands '''
    def __init__(self, commands):
        # building a list from the commands arguments ensures that it is iterable and keeps a local copy of the command references in each MacroCommand instance
        self.commands = list(commands)
    
    def __call__(self):
        # When an instance of MacroCommand is invoked, each command in self.commands is called in sequence
        for command in self.commands:
            command()

'''
Take a look at design pattern books/resources when finished with Fluent Python . . . 
'''