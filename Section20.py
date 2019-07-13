'''
Attribute Descriptors

Descriptors are a way of reusing the same access logic in MULTIPLE attributes
    is a class which implements a protocol consisting of the __get__, __set__ and __delete__ methods

property class implements the full descriptor protocol (partial implementations are OK)
MOST descriptors implement only __get__ and __set__ and MANY implement ONLY one of these methods

*Besides properties, other Python features that leverage descriptors are methods, classmethod, and staticmethod decorators


Descriptor example: attribute validation

Property factory is a way to AVOID repetitive coding of getters and setters by applying functional programming patterns
    higher order function that creates a parametrized set of accessor functions and builds a custom property instance from them with, with closures to hold settings like "storage_name" from the example in Section19

An alternative way to solve repetitive coding is by utilizing Descriptors


LineItem take #3: a simple descriptor
A class implementating a __get__, __set__ or a __delete__ method is a descriptor

create a Quantity descriptor and the LineItem class will use TWO instances of Quantity: one for managing the weight attribute and the other for price
    TWO weight attributes:
        1. class attribute of LineItem
        2. instance attribute that will exist in each LineItem object

descriptor class
    a class implementing the descriptor protocol
managed class
    the class where the descriptor instances are declared as class attributes
descriptor instance
    each instance of a descriptor class, declared as a class attribute of the managed class
managed instance
    one instance of the managed class
storage attribute
    an attribute of the managed instance which will hold the value of a managed attribute for that particular instance; these are distinct from the descriptor instances, which are ALWAYS class attributes
managed attribute
    a public attribute in the managed class that will be handled by a descriptor instance, with values stored in storage attributes. In other words, a descriptor instance and a storage attribute provide the infrastructure for a managed attribute

look at the MGN diagram on page 654
'''

# take a look at bulkfood_v3.py

'''
when coding a __set__ method you MUSt keep in mind what the "self" and "instance" arguments mean
    "self" is the descriptor instance (class attribute of the managed class)
    "instance" is the managed instance
*Descriptors managing instance attributes should store valaues in the managed instances

A drawback is the need to REPEAT the names of the attributes when the descriptors are instantiated in the managed class body
    NOTE: remember that the expression on the right side is ALWAYS evaluated first before the variable exists

problem: a typo like "price = Quantity('weight')" can lead the program to misbehave badly

solution to the repeated name problem can be presented in the following LineItem take shown below


LineItem take #4: automatic storage attribute names

solution: avoid retyping the attribute name in the descriptor declarations by generating a UNIQUE string for the storage_name of each Quantity instance

concatenate: '_Quantity#' and an integer (current value of a Quantity.__counter class attribtue) that we'll increment every time a new Quantity descriptor instance is attached to a class

* "#" character guarantees the storage_name will NOT clash with attributes created by the user using dot nation
'''

# take a look at bulkfood_v4.py and read the notes at the bottom

# take a look at bulkfood_v4b.py
# take a look at model_v4c.py 

# take a look at bulkfood_v4c.py and look at the testing at the bottom

# compare bulkfood_v4c.py to bulkfood_v4.py

'''
tips:
    usually we do NOT define a descriptor in the same module where it is used but in a SEPERATE utility module (model_v4c.py)

*automatically assigning storage names that resemble the managed attribute names REQUIRES a class decorator or a metaclass (covered in Section21)


Property factory vs. Descriptor class
'''

# take a look at bulkfood_v4prop.py

'''
The descriptor class approach is MORE appealing than the property factory for two reasons:
    1. a descriptor class can be extended by subclassing; reusing code from a factory function without copying and pasting is much HARDER

    2. it's more straightforward to hold state in class and instance attributes than in function attributes and closures as we did in bulkfood_v4prop.py

*property factory pattern is simpler in some regards; but the descriptor class appraoch is more extensible therefore it is more WIDELY used


LineItem take #5: a new descriptor type
'''