'''
Dynamic attributes and properties

data attributes and methods are collectively known as attributes
    a method is just an attribute that is callable

properties: can be used to replace a public data attribute with accessor methods (getter/setter) WITHOUT changing the class interface

__getattr__ & __setattr__
    evaluates attribute access using dot notation
        ie. obj.attr


Data wrangling with dynamic attributes
take a look at osconfeed.json
    shows 4 out of the 895 records in the JSON feed
    "serial" is the unique identifier within the list
'''

# take a look at osconfeed.py

'''
Exploring JSON-like data with dynamic attributes

the syntax feed: ['Schedule']['events'][40]['name'] is lengthy and annoying to read

in js; we can simply find our query with: "feed.Schedule.events[40].name"
    we can also implement a dict-like class that does the same in Python
'''

# take a look at class FrozenJSON in explore0.py
# take a look at explore_doctest.py

'''
**Any script that generates or emulates dynamic attribute names from arbitrary source MUST deal with one issue: the keys in the original data may NOT be suitable attribute names


The invalid attribute name problem 

FrozenJSON class has a limitation: there is NO special handling for attributes names that are Python keywords

look at the example below on attempting to retrieving the class value of the FrozenJSON object
'''

# # example - class is a reserved word in Python

# from Sec19_examples.explore0 import FrozenJSON
# grad = FrozenJSON({'name':'Jim Bo', 'class': 1982})

# # print(grad.class)
# # #                    ^
# # # SyntaxError: invalid syntax

# print(getattr(grad, 'class'))
# # 1982

'''
FrozenJSON was created to provide convenient access to the data.
a BETTER solution is checking whether a key in the mapping given to FrozenJSON.__init__ is a keyword and if so, append an _ to it, so the attribute can be read like the following:
'''

# print(grad.class_)
# # 1982

# take a look at explore1.py

# example - another problem may arise if a key in the JSON is NOT a valid Python identifier:
# x = FrozenJSON({'2be':'or not'})
# # print(x.2be)
# #             ^
# # SyntaxError: invalid syntax

'''
problematic keys like the one above are easy to detect because the str class provides the s.isidentifier() method which tells you whether s is a valid Python identifier
    *difficult process

solutions:
    1. raising an exception
    2. replace invalid key with generic names like attr_0, attr_1 and so on

logic of the build class method, which is used by __getattr__, returns a different type of object depending on the value of the attribute being accessed
    *instead of a class method, let's implement the __new__ special method


Flexible object creation with __new__
__new__ is a class method (gets special treatment; the @classmethod is NOT used) that returns an instance
    instance will in turn be passed as the first argument "self" of __init__

*since __init__ gets an instance when called, it is FORBIDDEN from returning anything (initializer)

__new__ is RARELY coded because the implementation is inherited from "object" suffices
    can also return an instance of a different class and when that happens, the interpreter does NOT call __init__

take a look at the pseudocode below
'''

# # pseudocode for object construction
# def object_maker(the_class, some_arg):
#     new_object = the_class.__new__(some_arg)
#     if isinstance(new_object, the_class):
#         the_class.__init__(new_object, some_arg)
#     return new_object

# # following statement are roughly equivalent
# x = Foo('bar')
# x = object_maker(Foo, 'bar')

# take a look at explore2.py and read the notes at the bottom

'''
Restructuring the OSCON feed with shelve

pickle is the name of the Python object serialization format
shelve module converts objects to/from pickle format

shelve modules provides pickle storage

shelve.open returns a shelve.Shelf instance - a simple key-value object database backed by the dbm module with the following characteristics:
    -shelve.Shelf subclasses abc.MutableMapping, so it provides the essential methods we expect of a MAPPING type
    -shelve.Shelf provides a few other IO management methods like sync and close; it's also a context manager
    -Keys and values are saved whenever a new value is assigned to a key
    -Keys must be strings
    -Values must be objects that the pickle module can handle

shelves provides a simple, efficient way to reorganize the OSCON schedule data: 
    -read all records from the JSON file and save them to a shelve.Shelf 
        -each key will be made from the record type and the serial number (event, 33950)
        -value will be an instance of a new Record class
'''

# take a look at schedule1.py
# take a look at schedule1_doctests.py

'''
Record.__init__ illustrated a Python hack; __dict__ of an object is where the attributes are kept
    updating an instance __dict__ with a mapping is a quick way to CREATE a bunch of attributes in that instance

1. FrozenJSON works by RECURSIVELY converting the nested mappings and lists; Record does NOT need that because our converted dataset does NOT have mappings nested in mappings or lists (records contain ONLY strings, integers, list of strings, and list of integers)

2. FrozenJSON provides access to the embedded __data dict attributes - which we used to invoke methods like keys - and now we do NOT need that functionality either

Record class object highlights the idea: __init__ updating the instance __dict__


Linked record retrievel with properties

goal of schedule2.py: given an event record retrieved from the shelf, reading its venue or speakers attributes will NOT return serial number but FULL-FLEDGED record objects

take a look at figure 19-1 on page 626: classes overview
    Record
        the __init__ method is the same as in schedule1.py; the __eq__ method was added to faciliate testing

    DbRecord
        Subclass of Record adding a __db class attribute, set_db and get_db static methods to set/get that attribute, a fetch class method to retrieve records from the database and a __repr__ instance method to support debugging and testing
            *coded __db as a PRIVATE class attribute with conventional getter and setter methods to PROTECT them from accidental overwriting
            **properties are class attributes designed to manage instance attributes

    Event
        Subclass of DbRecord adding venue and speakers properties to retrieve linked records, and specialized __repr__ method

DbRecord.__db class attribute exists to hold a reference to the opened shelve.Shelf database:
    DbRecord.fetch method 
    Event.venue
    Event.speakers 
'''

# take a look at schedule2.py (part 1: class Record)

'''
"new style" class are simply a user defined type

python2 ONLY: only "new-style" classes support properties; to write a new style class in Python2 - you MUST subclass directly/indirectly from object
    class Record(object):

python3: whether or not you subclass from object; all classes are "new-style"
'''

# take a look at schedule2.py (part 2: MissingDatabaseError and DbRecord class)
# take a look at schedule2.py (part 3: the Event class)

'''
in the venue property, the last line returns self.__class__.fetch(key) 
    self.fetch(key) ONLY works with the specific data set of the OSCON feed because is there NO event record with a 'fetch' key
        if a single event record had a key named 'fetch', then within that specific Event instance, the reference self.fetch would retrieve that VALUE of that field instead of the fetch CLASS method that Event inherits from DbRecord
'''

# take a look at schedule2 (part 4): the load_db function

'''
if classes named Speaker or Venue are coded, load_db will automatically use those classes when building and saving records, instead of the default DbRecord class

schedule2.py exemplified variety of techniqueues for implementing dynamic attributes using __getattr__, hasattr, getattr, @property, and __dict__
'''

# take a look at schedule2_doctests.py


'''
Using a property for attribute validation

LineItem take #1: class for an item in an order
    problem: negative #s results in a negative subtotal
    solution: 
        1. change the interface of LineItem to use a getter/setter for the weight attribute (java way)
        2. set the weight of an item by just assigning it; replace the data attribute with a PROPERTY (python way)
'''

# take a look at bulkfood_v1.py


'''
LineItem take #2: a validating property

implementing a property will ALLOW us to use a getter and a setter but the interface of LineItem will NOT change
    ie. setting the weight of a LineItem will still be written as 
'''

# take a look at bulkfood_v2.py

'''
we have protected weight from users providing negative values

problem: a bug may create a LineItem with a negative price
solution: we could also turn price into a property (this would entail some repetition)

"The cure for repetition is abstraction"

Two ways to abstract away property definitions:
    1. use a property factory
    2. descriptor class (more flexible)


A proper look at properties

property built-in is a class
the full signature of property:
    property(fget=None, fset=None, fdel=None, doc=None)
        -all args are optional
        -if function is NOT provided for one of them, the corresponding operation is NOT allowed by the resulting property object
'''

# take a look at bulkfood_v2b.py

'''
in a class body with MANY methods, the decorators make it explicit which are the getters and setters, without depending on the convention of using get and set prefixes in their name


Properties override instance attributes

properties are class attributes that manage attribute access in the instances of classes

recall that when an instance and a class both have a data attribute by the same name, the INSTANCE attribute overrides the class attribute

take a look at the example below
'''
# # example: instance attribute shadows class data attribute

# # define Class with TWO class attributes: the "data" data attribute and the prop property
# class Class:
#     data = 'the class data attr'
#     @property
#     def prop(self):
#         return 'the prop value'

# obj = Class()

# # vars returns the __dict__ of obj, showing it has NO instance attributes
# print(vars(obj))
# # {}

# # reading from obj.data rerieves the value of Class.data
# print(obj.data)
# # the class data attr

# # writing to obj.data CREATES an instance attribute
# obj.data = 'bar'

# # inspect the instance to see the instance attribute
# print(vars(obj))
# # {'data': 'bar'}

# # now reading from obj.data retrieves the value of the instance attribute. when read from the obj instance, the instance data shadows the class data
# print(obj.data)
# # bar

# # the Class.data attribute is intact
# print(Class.data)
# # the class data attr

'''
now let's try to override the prop attribute (decorated with @property) on the obj instance
'''

# # example - instance attribute does NOT shadow class property 

# # reading prop directly from Class retrieves the property object itself, WITHOUT running its getter method
# print(Class.prop)
# # <property object at 0x7f7be00adf98>

# # reading obj.prop executes the property getter
# print(obj.prop)
# # the prop value

# # trying to set an instance prop attribute fails
# # obj.prop = 'foo'
# # # AttributeError: can't set attribute

# # putting 'prop' DIRECTLY in the obj.__dict__ works
# obj.__dict__['prop'] = 'foo'

# # we can see that obj has TWO instance attributes: 'data' and 'prop'
# print(vars(obj))
# # {'data': 'bar', 'prop': 'foo'}

# # HOWEVER, reading obj.prop STILL runs the property getter. The property is NOT overshadowed by an instance attribute
# print(obj.prop)
# # the prop value

# # overwriting Class.prop DESTROYS the property object
# Class.prop = 'baz'

# # now obj.prop retrieves the INSTANCE attribute. Class.prop is NOT a property anymore, so it NO longer overrides "obj.prop"
# print(obj.prop)
# # foo

'''
add a new property to class and see it overriding an instance attribute
'''

# # example: new class property shadows existing instance attribute

# # obj.data retrieves the instance data attributes
# print(obj.data)
# # bar

# # Class.data retrieves the class data attribute
# print(Class.data)
# # the class data attr

# # Overwrite Class.data with a new property
# Class.data = property(lambda self: 'the "data" prop value')

# # obj.data is now shadowed by the Class.data property
# print(obj.data)
# # the "data" prop value

# # delete the property
# del Class.data

# # obj.data now reads the instance data attribute again
# print(obj.data)
# # bar

'''
the main point of these examples was to show that an expression like obj.attr does NOT search for attr starting with obj

BUT the search starts at obj.__class__, and only if there is NO property named attr in the class, Python looks in the obj instance itself

rule NOT only applies to properties but to a whole category of descriptors


Property Documentation

console's help() function or IDEs need to display the documentation of a property, they extract the information from the __doc__ attribute of the property
'''

# example of classic call syntax: property can get the documentation string as the doc argument

# weight = property(get_weight, set_weight, doc='weight in kilograms')

'''
when property is deployed as a decorator, the docstring of the getter method - the one with the "@property" decorator itself - is used as the documentation of the property as a whole (take a look at figure 19-2 on page 638)
'''

# example: documentation for a property

# class Foo:
    
#     @property
#     def bar(self):
#         ''' the bar attribute '''
#         return self.__dict__['bar']
    
#     @bar.setter
#     def bar(self, value):
#         self.__dict__['bar'] = value

# print(Foo.bar.__doc__)
# #  the bar attribute


'''
Coding a property factory

create a quantity property factory: the managed attributes represent quantities that can NOT be negative or zero in the application
'''

# take a look at bulkfood_v2prop.py
# take a look at the example testing at the bottom of bulkfood_v2prop.py

'''
note how the properties built by our factory act:
    the weight property overrides the weight instance attribute so that every reference of self.weight or nutmeg.weight is handled by the property functions, and the only way to BYPASS the property logic is to access the instance__dict__ directly

in real practical uses: 
    the quantity factory would be inside a utility module to be used over and over again

*this can be further refactored into a descriptor class (section 20)


Handling attribute deletion

deleting attributes is NOT something we do every day and the requirement to handle it with a property is even more UNUSUAL

@my_property.deleter decorator is used to wrap the method in charge of deleting the attribute managed by the property
'''

# take a look at blackknight.py
# then take a look at blackknight_doctests.py

'''
using the class call syntax instead of decorators, the fdel argument is used to set the DELETER function
    ie. member = property(member_getter, fdel=member_deleter)

attribute deletion can ALSO be handled by implementing the lower level __delattr__ special method


Essential attributes and functions for attribute handling
'''

# take a look at essentialattributes.txt

'''
using properties or descriptors is LESS error prone than defining these special methods
'''