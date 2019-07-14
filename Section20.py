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
when coding a __set__ method you MUST keep in mind what the "self" and "instance" arguments mean
    "self" is the descriptor instance (class attribute of the managed class)
    "instance" is the managed instance
*Descriptors managing instance attributes should store values in the managed instances

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

*property factory pattern is simpler in some regards; but the descriptor class approach is more extensible therefore it is more WIDELY used


LineItem take #5: a new descriptor type

Problem: LineItem instance was created with a blank description and the order could NOT be fulfilled

Solution: new descriptor NewBlank (only tweak the validation logic; the rest is the same as the Quantity descriptor)

Two different things than Quantity:
    1. takes care of the storage attributes in the managed instances
    2. validates the value used to set those attribute

Two base classes:
    AutoStorage
        Descriptor class which manages storage attributes automatically
    Validated
        AutoStorage abstract subclass that overrides __set__ method, calling a "validate" method which MUST be implemented by subclasses

AutoStorage base class
    manages the automatic storage of the attribute
Validated
    handles validation by delegating to an abstract "validate" method
Quantity and NonBlank
    concrete subclasses of Validated

The relationship between Validated, Quantity, and NonBlank is an application of the "Template Method" design pattern

A template method defines an algorithm in terms of abstract operations that subclasses override to provide concrete behavior
'''

# take a look at model_v5.py
# take a look at bulkfood_v5.py

'''
LineItem examples demonstrate a typical use of descriptors to manage data attributes

Overriding descriptors is a descriptor that has a __set__ method that overrides the setting of an attribute by the same name in the managed instance


Overriding vs. Non-Overriding descriptors

Asymmetry with handling attributes:
    1. Reading an attribute through an instance normally returns the attribute defined in the instance, but if there is NO such attribute in the instance, a class attribute will be retrieved

    2. On the other hand, assigning to an attribute in an instance normally creates the attribute in the instance, without affecting the class
'''

# take a look at descriptorkinds.py 

'''
Overriding descriptor
    a descriptor that implements the __set__ method; will override attempts to assign to instance attributes

properties are an example of overriding descriptors: if you do NOT provide a setter function, the default __set__ from the property class will raise an AttributeError
'''

# # example (refer to descriptorkinds.py) - behavior of an overriding descriptor: obj.over is an instance of Overriding

# from Sec20_examples.descriptorkinds import *

# # create Managed object for testing
# obj = Managed()

# # obj.over triggers the descriptor __get__ method, passing the managed instance obj
# obj.over
# # -> Overriding._get_(<Overriding object>, <Managed object>, <class Managed>)

# # Managed.over triggers the descriptor __get__ method, passing None as the second argument (instance)
# Managed.over
# # -> Overriding._get_(<Overriding object>, <NoneType object>, <class Managed>)

# # Assigning to obj.over triggers the descriptor __set__ method, passing the value 7 as the last argument
# obj.over = 7
# # -> Overriding._set_(<Overriding object>, <Managed object>, <int object>)

# # Reading obj.over still invokes the descriptor __get__ method
# obj.over
# # -> Overriding._get_(<Overriding object>, <Managed object>, <class Managed>)

# # Bypassing the descriptor, setting a value directly to the obj.__dict__
# obj.__dict__['over'] = 8
# # Verify that the value is in the obj.__dict__, under the over key
# print(vars(obj))
# # {'over': 8}

# # However, even with an instance attribute named over, Managed.over descriptor still overrides attempts to read obj.over
# obj.over
# # -> Overriding._get_(<Overriding object>, <Managed object>, <class Managed>)


'''
Overriding descriptor without __get__

possible for overriding descriptors to implement only __set__
    only writing is handled by the descriptor

    reading the descriptor thorugh an instance will return the DESCRIPTOR OBJECT ITSELF because there is no __get__ to handle that access

namesake (instance attribute that shares the same name as a class attribute) instance attribute:
    if created with a new value via direct access to the instance __dict__, the __set__ method will OVERRIDE further attempts to set that attribute

    reading that attribute will return the new value from the instance, INSTEAD of returning the descriptor object
'''

# # example (refer to descriptorkinds.py) - overriding descriptor without __get__: obj.over_no_get is an instance of OverridingNoGet

# from Sec20_examples.descriptorkinds import *

# obj = Managed()

# # this overriding descriptor does NOT have a __get__ method, so reading obj.over_no_get retrieves the descriptor instance from the class
# print(obj.over_no_get)
# # <Sec20_examples.descriptorkinds.OverridingNoGet object at 0x7f1945ce09b0>

# # the same thing happens if we retrieve the descriptor instance directly from the managed class
# print(Managed.over_no_get)
# # <Sec20_examples.descriptorkinds.OverridingNoGet object at 0x7f92a953d9e8>

# # trying to set a value to obj.over_no_get invokes the __set__ descriptor method
# obj.over_no_get = 7
# # -> OverridingNoGet._set_(<OverridingNoGet object>, <Managed object>, <int object>)

# # since our __set__ doesn't make changes, reading obj.over_no_get again retrieves the descriptor instance from the managed class
# print(obj.over_no_get)
# # <Sec20_examples.descriptorkinds.OverridingNoGet object at 0x7fd19ac149e8>

# # going through the instance __dict__ to set an instance attribute named over_no_get
# obj.__dict__['over_no_get'] = 9
# print(obj.over_no_get)
# # 9

# # trying to assign a value to obj.over_no_get still goes through the descriptor set
# obj.over_no_get = 7
# # -> OverridingNoGet._set_(<OverridingNoGet object>, <Managed object>, <int object>)

# # but for reading, that descriptor is SHADOWED as long as there is a namesake instance attribute
# print(obj.over_no_get)
# # 9


'''
Non-overriding descriptor
    a descriptor that does NOT implement __set__

setting an instance attribute with the SAME name will SHADOW the descriptor, rendering it ineffective for handling that attribute in that specific instance

methods are implemented as NON-OVERRIDING descriptors
'''

# # example (refer to descriptorkinds.py) - Behavior of a non-overriding descriptor: obj.non_over is an instance of NonOverriding

# from Sec20_examples.descriptorkinds import *

# obj = Managed()

# # obj.non_over triggers the descriptor __get__ method, passing obj as the second argument
# obj.non_over
# # -> NonOverriding._get_(<NonOverriding object>, <Managed object>, <class Managed>)

# # Managed.non_over is a NON-overriding descriptor, so there is NO __set__ to interfere with this assignment
# obj.non_over = 7

# # The obj now has an instance attribute named non_over which SHADOWS the namesake descriptor attribute in the Managed class
# print(obj.non_over)
# # 7

# # the Managed.non_over descriptor is still there, and catches this access via the class
# Managed.non_over
# # -> NonOverriding._get_(<NonOverriding object>, <NoneType object>, <class Managed>)

# # if the non_over instance attribute is deleted ...
# del obj.non_over

# # then reading obj.non_over hits the __get__ method of the descriptor in the class, but NOTE that the second argument is the managed instance
# obj.non_over
# # -> NonOverriding._get_(<NonOverriding object>, <Managed object>, <class Managed>)

'''
overriding descriptors are also called data descriptors or enforced descriptors

Non-overriding descriptors are also called non-data descriptors or shadowable descriptors

The setting of attributes in the class CANNOT be controlled by descriptors attached to the same class


Overwriting a descriptor in the class

regardless of whether a descriptor is overriding or not, it CAN be overwrriten by assignment to the class
    monkey patching technique that effectively breaks any class that depends on the descriptors for proper operation
'''

# example: any descriptor can be OVERWRITTEN on the class itself

# from Sec20_examples.descriptorkinds import *

# # create a new instance
# obj = Managed()

# # overwrite the descriptor attributes in the class
# Managed.over = 1
# Managed.over_no_get = 2
# Managed.non_over = 3

# # the descriptors are really gone
# print((obj.over, obj.over_no_get, obj.non_over))
# # (1, 2, 3)

'''
the reading of a class attribute can be controlled by a descriptor with __get__ attached to the managed class

the writing of a class attribute CANNOT be handled by a descriptor with __set__ attached to the same class


Methods are descriptors

a function within a class becomes a BOUND method because all user-defined functions have a __get__ method, therefore they operate as descriptors when attached to a class
'''

# # example - a method is a non-overriding descriptor

# obj = Managed()

# # reading from obj.spam retrieves a BOUND method object
# print(obj.spam)
# # <bound method Managed.spam of <Sec20_examples.descriptorkinds.Managed object at 0x7fee6fe0d978>>

# # but reading from Managed.spam retrieves a function
# print(Managed.spam)
# # <function Managed.spam at 0x7f7db4f1a730>

# # assigning a value to obj.spam SHADOWS a class attribute, rendering the spam method inaccessible from the obj instance
# obj.spam = 7
# print(obj.spam)
# # 7

'''
functions do NOT implement __set__, they are NON-OVERRIDING descriptors

NOTE: obj.spam & Managed.spam retrieve different objects

__get__ of a function returns a reference to itself when the access happens through the managed class

when the access goes through an instance:
    the __get__ of the function returns a BOUND method object: a callable which wraps the function and BINDS the managed instance (ie. obj) to the first argument of the function (ie. self)
'''

# take a look at method_is_descriptor.py
# take a look at the experiments we did on the bottom method_is_descriptor.py

'''
bound method object has a __call__ method
    handles the actual invocation
    
    calls the original function referenced in __func__, passing the __self__ attribute of the method as the first argument


Descriptor usage tips

1. Use property to keep it simple
    *the property built-in creates OVERRIDING descriptors that implement both __set__ and __get__ (even if setter method is NOT defined)
    *default __set__ of a property raises AttributeError: can't set attribute, so a property is the easiest way to create a READ-ONLY attribute

2. Read-only descriptors require __set__
    *must remember to code BOTH __get__ and __set__ when using a descriptor class to implement a READ-ONLY attribute
    *setting a namesake attribute on an instance will SHADOW the descriptor
    *__set__ method of a READ-ONLY attribute should just raise AttributeError with a message

3. Validation descriptors can work with __set__ only
    *in a descriptor designed ONLY for validation, the __set__ method should check the value argument it gets and if VALID, set it directly in the instance __dict__ using the descriptor instance name as key
        *reading the attribute with the same name from the instance will be as fast as possible, as it will NOT require a __get__

4. Caching can be done effectively with __get__ only
    *if you code just the __get__ method, you have a NON-OVERRIDING descriptor
    *useful to make some expensive computation and then CACHE the result by setting an attribute by the same name on the instance
    *namesake instance attribute will SHADOW the descriptor so subsequent access to that attribute will fetch it DIRECTLY from instance __dict__ and NOT trigger the descriptor __get__ anymore

5. Non-special methods can be shadowed by instance attributes
    *functions and methods only implement __get__, they do NOT handle attempts at setting instance attributes with the same name
        ie. my_obj.the_method = 7 means that further access to the_method through that method will retrive the number 7 - WITHOUT affecting the class or other instances

    *NO issue with SPECIAL METHODS:
    *Interpreter ONLY looks for special methods in the class itself:
        ie. repr(x) is executed as x.__class__.__repr__(x), so a __repr__ attribute defined in x has NO effect of repr(x)

    *class methods are SAFE as long as they are accessed THROUGH the class (FrozenJSON.build)
    *Special methods, class methods, static methods, and properties are all SAFE from this issue
        NOTE: properties are data descriptors, so CANNOT be overriden by instance attributes


Descriptor docstring and overriding deletion

docstring of a descriptor class is used to document every instance of the descriptor in the managed class
*customizing the help text for each descriptor instance is difficult
    ie. the same Quantity descriptor class is used for weight and price

descriptors: handling attempts to delete a managed attribute can be done by implementing a __delete__ method alongside or instead of the usual __get__ and/or __set__ in the descriptor class
'''
