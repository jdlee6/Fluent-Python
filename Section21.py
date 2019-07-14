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
class Dog:
    def __init__(self, name, weight, owner):
        self.name = name
        self.weight = weight
        self.owner = owner

rex = Dog('Rex', 30, 'Bob')
# repr not functional; ugly
print(repr(rex))
# <__main__.Dog object at 0x7f677f5bbb00>

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

# example for display purposes only - type

class MyClass(MySuperClass, MyMixin):
    x = 42

    def x2(self):
        return self.x*2

# functionally equivalent to each other

MyClass = type('MyClass', (MySuperClass, MyMixin), {'x': 42, 'x2': lambda self: self.x*2})

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
    -subclasses of decorated class may or may NOT inherit the changed made by the decorator


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
the main point of scenario#2 is to show that the effects of a class decorator MAY affect subclasses

...
'''
