'''
Class metaprogramming
    art of creating or customizing class at RUN time

metaclasses let you create whole new categories of classes with special traits, such as the abstract base classes

*difficult to justify in real code because most class decorators solve many of the problems
**if you are NOT authoring a framework, you should NOT be writing metaclasses


A class factory

a class factory is something like collections.namedtuple
    a function that, given a class name and attribute names, creates a subclass of tuple that allows retrieving items by name and provides a __repr__ for debugging
'''

# example: bad way of writing a way to process data for dogs as simple records in a pet shop app
# class Dog:
#     def __init__(self, name, weight, owner):
#         self.name = name
#         self.weight = weight
#         self.owner = owner

# rex = Dog('Rex', 30, 'Bob')
# # repr not functional; ugly
# print(repr(rex))
# # <__main__.Dog object at 0x7f677f5bbb00>

'''
create a record_factory that creates simple classes like Dogs on the fly
'''

# take a look at record_factory.py
# take a look at record_factory_doctests.py

'''
type is typically thought of as a function but type is actually a class - it behaves like a class that CREATES a new class when invoked with three arguments
    three arguments of type are: 
        name
        bases
        dict
'''

# # example for display purposes only - type

# class MyClass(MySuperClass, MyMixin):
#     x = 42

#     def x2(self):
#         return self.x*2

# # functionally equivalent to each other

# MyClass = type('MyClass', (MySuperClass, MyMixin), {'x': 42, 'x2': lambda self: self.x*2})

'''
NOTE: instances of type are classes
    ie. MyClass from the above example
         Dog class in record_factory_doctests.py

the last line of record_factory BUILDS a class named by the value of cls_name, object as its single immediate superclass and with attributes named __slots__, __init__, __iter__ and __repr__ (last 3 are instance methods)

invoking type with 3 arguments is a common way of creating a class DYNAMICALLY

instances of classes created by record_factory have a LIMITATION:
    -NOT serializable
        ie. can't be used with dump/load functions from the pickle module
https://docs.python.org/3/library/pickle.html#pickle.dump


A class decorator for customizing descriptors

recall how values of attributes such as "weight" was stored in an instance attribute named "_Quantity#0"
    caused debugging to be a bit challenging
    ie. LineItem.weight.storage_name --> '_Quantity#0'

it would be better if the storage names included the name of the managed attribute:
    ie. LineItem.weight.storage_name --> '_Quantity#weight'

once the whole class is assembled and descriptors are BOUND to class attributes, we can inspect the class and SET proper storage names to the descriptor
    -could be done with __new__ BUT wasted effort because the logic of __new__ will run every time a new LineItem instance is created BUT the binding of the descriptor to the managed attribute will NEVER change once the LineItem class itself is built

    -solution: NEED to set the storage names when the class is created; this is where class decorators or metaclass play their part

a class decorator is a function that gets a class object and returns the same class or a modified one
'''

# take a look at model_v6.py
# take a look at bulkfood_v6.py
# take a look at doctests at the bottom of bulkfood_v6.py

'''
class decorators are a simpler way of doing something that previously required a metaclass: customizing a class the moment it's created

Drawback of class decorators:
    -ONLY act on the class where they are directly applied
    -subclasses of decorated class may or may NOT inherit the changes made by the decorator


What happens when: import time versus. run time

MUST be aware when the Python interpreter evaluates each block of code

import time
    -the interpreter parses the source code of a .py module in one pass from top to bottom and generates the bytecode to be executed (syntax error may occur here)
    -import statement actually runs ALL the top level code of the imported module when it's imported for the first time in the process
    **the import statement can trigger all sorts of "run time" behavior**

    top level code:
        -the interpreter defines top level functions at IMPORT time but executes their body only when - and if - the functions are invoked at RUN time

Classes (different) @ import time: 
    -the interpreter executes the BODY of EVERY class, even the body of classes nested in other classes. 
    -execution of a class body means that the attributes and methods of the class are defined and then the class object is built
    -body of classes = "top level code" because it runs at IMPORT time


The evaluation of time exercises

evaltime.py imports a module evalsupport.py
    both modules have several print calls to output markers in the format <[N]>, where N is a number
'''

# look at time_exercise.txt: determine when each of these calls will be made (refer to evaltime.py and evalsupport.py)

'''
the main point of scenario#2 is to show that the effects of a class decorator may NOT affect subclasses

in the example above: 
    ClassFour is a subclass of ClassThree; the @deco_alpha decorator is applied to ClassThree, which replaces its method_y, but that did NOT affect ClassFour at all
        *if ClassFour.method_y invoked ClassThree.method_y with super(), then we would've seen the effect of the decorator


Metaclasses 101

A metaclass is a class that builds classes
    is a class factory, EXCEPT that instead of a function (like record_factory), a metaclass is written as a CLASS
'''

# example: Python classes are instances of type; type is the metaclass for most built-in and user defined classes

# print('spam'.__class__)
# # <class 'str'>

# print(str.__class__)
# # <class 'type'>

# from Sec21_examples.bulkfood_v6 import LineItem
# print(LineItem.__class__)
# # <class 'type'>

# print(type.__class__)
# # <class 'type'>

'''
the examples above say the both "str" and "LineItem" are INSTANCES of "type"
    ALL are subclasses of "object"

take a look at figure 21-2 on pg. 694 (both diagrams are true)
    1. str, type and LineItem are subclasses of "object"
    2. str, object, and LineItem are instances of type, because they are all classes

classes object and type have a UNIQUE relationship:
    "object" is an INSTANCE of "type" & "type" is a SUBCLASS of "object"

few other metaclasses exist in the standard library such as ABCMeta and Enum
'''

# example: the class of collections.Iterable is abc.ABCMeta. The class Iterable is abstract, BUT ABCMeta is NOT; Iterable is an INSTANCE of ABCMeta

import collections, abc

print(collections.Iterable.__class__)
# <class 'abc.ABCMeta'>

print(abc.ABCMeta.__class__)
# <class 'type'>

print(abc.ABCMeta.__mro__)
# (<class 'abc.ABCMeta'>, <class 'type'>, <class 'object'>)

'''
every class is an instance of type but ONLY metaclasses are also subclasses of type

a metaclass, such as ABCMeta inherits from type the power to construct classes

take a look at figure 21-3 on pg 670
    1. Iterable is a subclass of object and an instance of ABCMeta
    2. BOTH object and ABCMeta are instances of type
    3. ABCMeta is also a subclass of type because ABCMeta is a metaclass
    4. Iterable is the ONLY abstract class

*ALL classes are INSTANCES of type, but metaclasses are SUBCLASSES of type, so they act as class factories
    a metaclass can customize its instances by implementing __init__
        __init__ method can do EVERYTHING a class decorator can do


The metaclass evaluation time exercise
'''

# look at time_meta.txt: determine when each of these calls will be made (refer to evaltime_meta.py)

'''
NOTE: when coding a metaclass, it's conventional to replace "self" with "cls"
    makes it clear that the instance under construction is a class


A metaclass for customizing descriptors
'''

# take a look at model_v7.py
# take a look at bulkfood_v7.py

'''
this only works because model_v7.py DEFINES a metaclass and model.Entity is an INSTANCE of that metaclass

even though the support module, model_v7.py, is HARDER to understand than model_v6.py - the user level code is SIMPLER: 
    just inherit from model_v7.entity and you get custom storage names for your Validated fields


The metaclass __prepare__ special method (only from Python 3+)

BOTH the "type" constructor & "__new__ and __init__" methods of metaclasses RECEIVE the body of the class evaluated as a mapping of names to attributes

    Problem:by DEFAULT: that mapping is a dict, which means the ORDER of the attributes as they appear in the class body is LOST 

    Solution: __prepare__ method
        is relevant ONLY in metaclasses and it MUST be a class method that must be defined with the @classmethod decorator

        invoked by the interpreter before the __new__ method in the metaclass to create the mapping that will be filled with the attributes from the class body

        __prepare__ gets the "metaclass" as the first argument and then gets the "name" of the class to be constructed and its tuple of "base" classes and MUST return a mapping which will be received as the last argument by __new__ and then __init__ when the metaclass builds a new class
'''

# take a look at model_v8.py
# take a look at bulkfood_v8.py

'''
in real world, metaclasses are used in frameworks/libraries for:
    -attr. validation
    -applying decorators to many methods at once
    -object serialization or data conversion
    -object relational mapping
    -object based persistency
    -dynamic translation of class structures from other languages


Classes as objects (special attributes)

every class has a number of attributes
    we've seen some already: __mro__, __class__, __name__

    cls.__bases__
        the tuple of base classes of the class

    cls.__qualname__
        a new attr. in Python 3.3 holding the qualified name of a class or function, which is a dotted path from the global scope of the module to the class definition
        
        ie. class ClassOne():
                ...
                class ClassTwo(object):
                    ...
        
        the __qualname__ of the inner class ClassTwo would be the string 'ClassOne.ClassTwo', while its __name__ is just 'ClassTwo'

    cls.__subclasses__()
        method returns a list of the immediate subclasses of the class. implementation uses WEAK references to avoid circular references between the superclass and its subclasses - which hold a STRONG reference to the superclasses in their __bases__ attribute. The method returns a LIST of subclasses that currently exist in memory

    cls.mro()
        the interpreter calls this method when building a class to obtain the tuple of superclasses that is stored in the __mro__ attribute of the class.

**NONE of these attributes mentioned in this section are listed by the dir(...) function**
'''
