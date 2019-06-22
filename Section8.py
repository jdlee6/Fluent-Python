'''
Object references, mutability and recycling

Variables are not boxes
Python variables are reference variables - think of them as labels attached to objects

because variables are labels; NOTHING prevents an object from having several labels assigned to it; if this happens this is referred to as Aliasing
'''

# example - variables a and b hold references to the same list, not copies of the list

# a = [1, 2, 3]
# b = a
# a.append(4)
# print(b)
# # [1, 2, 3, 4]

# # example - variables are assigned to objects only after the objects are created
# class Gizmo:
#     def __init__(self):
#         print('Gizmo id: %d' % id(self))
# x = Gizmo()
# print(x)
# the output Gizmo id: ... is a side effect of creating a Gizmo instance
# Gizmo id: 140665618674576
# <__main__.Gizmo object at 0x7fef443bb390>

# Multiplying a Gizmo instance will raise an exception
# y = Gizmo() * 10
# print(y)
# Here is proof that second Gizmo was actually instantiated before the multiplication was attempted
# Gizmo id: 140665618675192
# TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'

# but variable y was never created, because the exception happened while the right-hand side of the assignment was being evaluated
# print(dir())
# ['Gizmo', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b', 'x']


##########################################################################################

'''
Identity, equality and aliases

aliases: two variables that are bound to the SAME object
"every object has an identity, type and a value"
    -is operator compares the identity of the two objects
        -identity checks are most often done with the is operator
    -id() function returns an integer representing its identity
        -returns the memory address of the object; unique numeric label that will NEVER change during the life of the object
'''

# example - charles and lewis refer to the SAME object (aliasing)

# charles = {'name': 'Charles L. Dodgson', 'born': 1832}
# # lewis is an alias for charles
# lewis = charles

# # the is operator 
# print(lewis is charles)
# # True

# # and the id function confirm it
# print(id(charles), id(lewis))
# # 139783303278952 139783303278952

# # adding an item to lewis is the same as adding an item to charles
# lewis['balance'] = 950

# print(charles)
# # {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}


# # example - alex and charles compare equal BUT alex is NOT charles (these variables are bound to DISTINCT objects; same values but different identities)

# # alex refers to an object that is a replica of the object assigned to charles
# alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}

# # the objects compare equal, because of the __eq__ implementation in the dict class
# print(alex == charles)
# # True

# # but they are distinct objects. This is the Pythonic way of writing negative identity comparison: a is not b
# print(alex is not charles)
# # True

##########################################################################################

'''
Choosing between == and is 

the == operator compares the VALUES of objects (data they hold), while is compares their IDENTITIES
*often care about values and not identities; so == appears more frequently than is in Python code

*the is operator is faster than == because it CANNOT be overloaded
in contrast; a == b in other words mean a.__eq__(b); the __eq__ method inherited from object compares object ids so it produces the same result as is
    -equality may involve a lot of processing 
'''
# # example - to check if a variable is bound to None:
# x = None
# print(x is None)
# # True 

# print(x is not None)
# # False

'''
The relative immutability of tuples

if the referenced items are mutable; they may change if the tuple itself does NOT
immutability of tuples refers to the physical contents of the tuple data structure (references it holds) and does NOT extend to the referenced objects

Look at the example below:
'''

# example - t1 and t2 initially compare equal, but changing a mutable item inside tuple t1 makes it different

# # t1 is immutable, but t1[-1] is mutable (list is mutable)
# t1 = (1, 2, [30, 40])
# # build a tuple t2 whose items are equal to those of t1
# t2 = (1, 2, [30, 40])
# # although distinct objects, t1 and t2 compare equal, as expected
# print(t1 == t2)
# # True

# # inspect the identity of the list at t1[-1]
# print(id(t1[-1]))
# # 140492125183880

# # modify the t1[-1] list in place
# t1[-1].append(99)
# print(t1)
# # (1, 2, [30, 40, 99])

# # the identity of t1[-1] has NOT changed, only its value
# print(id(t1[-1]))
# # 140492125183880

# # t1 and t2 are now different
# print(t1 == t2)
# # False

'''
distinction between equality and identity has further implications when you need to copy an object
    -a copy is an equal object with a different id

Copies are shallow by default
'''
# example - easiest way to copy a list is to use the built-in constructor for the type itself
# l1 = [
#     3,
#     [55, 44],
#     (7, 8, 9)
# ]
# # list(l1) creates a copy of l1
# l2 = list(l1)
# print(l2)
# # [3, [55, 44], (7, 8, 9)]

# # copies are equal
# print(l2 == l1)
# # True

# # BUT refer to two different objects
# print(l2 is l1)
# # False

'''
for lists and other MUTABLE sequences, the shortcut l2 = l1[:] also makes a copy
    -using the constructor or [:] produces a SHALLOW copy 
        -ie: the outermost container is duplicated but the copy is filled with references to the same items held by the original container
        -causes no problems if all items are IMMUTABLE; but mutable items may cause problems

in the example below, we create a shallow copy of a list containing another list and tuple and then make changes to see how they affect the referenced objects
'''

# example - making a shallow copy of a list containing another list
# l1 = [
#     3,
#     [66, 55, 44],
#     (7, 8, 9)
# ]

# # l2 is a shallow copy of l1
# l2 = list(l1)

# # appending 100 to l1 has no effect on l2
# l1.append(100)

# # remove 55 from the inner list l1[1]; affects l2 because l2[1] is bound to the same list as l1[1]
# l1[1].remove(55)
# print('l1:', l1)
# print('l2:', l2)
# # l1: [3, [66, 44], (7, 8, 9), 100]
# # l2: [3, [66, 44], (7, 8, 9)]

# # for a mutable object like the list referred by l2[1], the operator += changes the list IN-PLACE. This change is visible at l1[1], which is an alias for l2[1]
# l2[1] += [33, 22]

# # += on a tuple creates a new tuple and rebinds the variable l2[2] here. This is the same as doing l2[2] = l2[2] + (10, 11) Now the tuples in the last position of l1 and l2 are NO longer the same object
# l2[2] += (10, 11)

# print('l1:', l1)
# print('l2:', l2)
# # l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
# # l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]

'''
Deep and shallow copies of arbitrary objects

deep copies are made for duplicates that do NOT share references of embedded objects

copy() vs deepcopy()
'''

# example - defines class Bus, representing a school bus that is loaded with passengers and then picks or drops passengers on its route

# class Bus:
#     def __init__(self, passengers=None):
#         if passengers is None:
#             self.passengers = []
#         else:
#             self.passengers = list(passengers)
    
#     def pick(self, name):
#         self.passengers.append(name)

#     def drop(self, name):
#         self.passengers.remove(name)

# # example continued - effects of using copy vs. deepcopy
# import copy

# bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
# bus2 = copy.copy(bus1)
# bus3 = copy.deepcopy(bus1)

# # using copy and deepcopy, we create three distinct Bus instances
# print(id(bus1), id(bus2), id(bus3))
# # 140544378607432 140544378607656 140544378608552

# bus1.drop('Bill')
# # after bus1 drops 'Bill', he is also missing from bus2
# print(bus2.passengers)
# # ['Alice', 'Claire', 'David']

# # inspection of the passengers attribute shows that bus1 and bus2 share the SAME list object, because bus2 is a SHALLOW copy of bus1
# print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
# # 140063737346952 140063737346952 140063737232648

# #bus3 is a deep copy of bus1, so its passengers attribute refers to another list
# print(bus3.passengers)
# # ['Alice', 'Bill', 'Claire', 'David']


# # example - Cyclic references: b refers to a, and then is appended to a; deepcopy still manages to copy a
# a = [10, 20]
# b = [a, 30]
# a.append(b)
# print(a)
# # [10, 20, [[...], 30]]

# from copy import deepcopy
# c = deepcopy(a)
# print(c)
# # [10, 20, [[...], 30]]


'''
Function parameters as references

call by sharing means that each formal parameter of the function gets a copy of each reference in the arguments
-parameters inside the function become aliases of the actual argument
'''

# example - a function may change any mutable object it receives

# def f(a, b):
#     a += b
#     return a

# x = 1
# y = 2
# print(f(x, y))
# # 3

# # the number x is unchanged
# print(x, y)
# # 1 2

# a = [1, 2]
# b = [3, 4]
# print(f(a, b))
# # [1, 2, 3, 4]

# # the list a is changed
# print(a, b)
# # [1, 2, 3, 4] [3, 4]

# t = (10, 20)
# u = (30, 40)
# print(f(t, u))
# # (10, 20, 30, 40)

# # the tuple t is unchanged
# print(t, u)
# # (10, 20) (30, 40)


'''
Mutable types as parameter defaults: bad idea

you should AVOID mutable objects as DEFAULT values for parameters

look at the example below:
    -instead of having a default value of passengers=None; we have passengers=[]
'''

# example - simple class to illustrate the danger of a mutable default

# class HauntedBus:
#     ''' a bus model haunted by ghost passengers '''
#     # when the passengers argument is not passed, this parameter is bound to the default list object, which is initially empty
#     def __init__(self, passengers=[]):
#         # this assignment makes self.passengers an alias for passengers which is itself an alias for the default list, when no passengers argument is given
#         self.passengers = passengers

#     def pick(self, name):
#         self.passengers.append(name)

#     def drop(self, name):
#         # when the methods .remove() and .append() are used with self.passengers we are actually mutating the default list, which is an attribute of the function object
#         self.passengers.remove(name)


# # example - buses haunted by ghost passengers
# bus1 = HauntedBus(['Alice', 'Bill'])
# # so far so good; no surprises with bus1
# print(bus1.passengers)
# # ['Alice', 'Bill']

# bus1.pick('Charlie')
# bus1.drop('Alice')
# print(bus1.passengers)
# # ['Bill', 'Charlie']

# # bus2 starts empty, so the default empty list is assigned to self.passengers
# bus2 = HauntedBus()
# bus2.pick('Carrie')
# print(bus2.passengers)
# # ['Carrie']

# # bus3 also starts empty, again the default list is assigned
# bus3 = HauntedBus()
# # the default is no longer empty
# print(bus3.passengers)
# # ['Carrie']

# bus3.pick('Dave')
# # Now Dave, picked by bus3, appears in bus2
# print(bus2.passengers)
# # ['Carrie', 'Dave']

# # the problem: bus2.passengers and bus3.passengers refer to the same list
# print(bus2.passengers is bus3.passengers)
# # True

# # bus1.passengers is a distinct list
# print(bus1.passengers)
# # ['Bill', 'Charlie']

'''
the problem is that Bus instances that don't get an initial passenger list end up SHARING the same passenger list among themselves

when the example above is instantiated with a list of passengers, it works as expected
problem is that each default value is evaluated when the function is defined and the default values become attributes of the function object
    -so if a default value is mutable object, and you change it, the change will affet every future call of the function
'''

# print(dir(HauntedBus.__init__))
# # ['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__

# print(HauntedBus.__init__.__defaults__)
# # (['Carrie', 'Dave'],)

# # we can verify that bus2.passengers is an alias bound to the first element of the HauntedBus.__init__.__defaults__attribute
# print(HauntedBus.__init__.__defaults__[0] is bus2.passengers)
# # True

# The issue with mutable defaults explains why None is often used as the default value for parameters that may receive mutable values

#########################################################################################################################

'''
Defensive programming with mutable parameters

Look at the example below to see how the TwilightBus class works from the perspective of a client of the class

*TwilightBus violates the "Principle of least astonishment", a best practice of interface design
'''

# example - passengers disappear when dropped by a TwilightBus

# # basketball_team holds five student names
# basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
# # a TwilightBus is loaded with the team
# bus = TwilightBus(basketball_team)
# # The bus drops one student and then another
# bus.drop('Tina')
# bus.drop('Pat')
# # The dropped passengers vanished from the basketball team
# print(basketball_team)
# # ['Sue', 'Maya', 'Diana']



# # example - simple class to show the perils of mutating received arguments
# class TwilightBus:
#     ''' a bus model that makes passengers vanish '''
#     def __init__(self, passengers=None):
#         # here we are careful to create a new empty list when passengers is None
#         if passengers is None:
#             # however this assignment makes self.passengers an alias for passengers which is itself an alias for the actual argument passed to __init__ - basketball_team (example above)
#             self.passengers = []
#         else:
#             self.passengers = passengers

#     def pick(self, name):
#         # when the methods .remove() and .append() are used with self.passengers, we are actually mutating the original list received as argument to the constructor
#         self.passengers.append(name)
    
#     def drop(self, name):
#         self.passengers.remove(name)

'''
the problem here is that the bus is ALIASING the list that is passed to the constructor. Instead, it should keep its OWN passenger list

solution: in __init__, when the passengers parameter is provided, self.passengers should be initialized with a copy of it

the method below will now NO longer affect the argument used to initialize the bus
solution is more flexible
    -argument passed to the passengers parameter may be a tuple or any other iterable like a set or even database results because the list constructor accepts any iterable
'''

# def __init__(self, passengers=None):
#     if passengers is None:
#         self.passengers = []
#     else:
#         # make a copy of the passengers list or convert it to a list if its not one
#         self.passengers = list(passengers)


#########################################################################################################################

'''
del and garbage collection

the del statement deletes names, NOT objects 
    -an object may be garbage collected as a result of del command but only if the variable deleted holds the last reference to the object or if the object becomes unreachable

rebinding a variable may also cause the number of references to an object reach zero, causing its destruction

del does NOT delete objects ,but objects may be deleted as a consequence of being unreachable after del is used (look at example below)
'''

# example - demonstrates the end of an object's life - uses weakref.finalize to register a callback function to be called when an object is destroyed

# import weakref
# s1 = {1, 2, 3}
# # s1 and s2 are aliases referring to the same set {1, 2, 3}
# s2 = s1

# # this function must NOT be a bound method the object about to be destroyed or otherwise hold a reference to it
# def bye():
#     print('Gone with the wind . . . ')

# # register the bye callback on the object referred by s1
# ender = weakref.finalize(s1, bye)
# # the .alive attribute is True before the finalize object is called
# print(ender.alive)
# # True

# del s1
# # as discussed, del does not delete an object, just a reference to it
# print(ender.alive)
# # True

# # rebinding the last reference, s2, makes {1, 2, 3} unreachable. It is destroyed, the bye callback is invoked and ender.alive becomes False
# s2 = 'spam'
# # Gone with the wind . . . 

# print(ender.alive)
# # False


'''
weak references

presence of references is what keeps an object alive
    -when the reference count reaches 0, the garbage collector disposes of it

weak references are useful in caching applications because you dont want the cached objects to be kept alive just because they are referenced by the cache
'''
# example - weakref.ref instance can be called to reach its referent. if the object is alive, calling the weak reference returns it, otherwise None is returned
# weak reference is a callable that returns the referenced object or None if the referent is no more
# example performed in Terminal/Console session; vs code displays different results

import weakref

a_set ={0, 1}
# the wref weak reference object is created and inspected in the next line
wref = weakref.ref(a_set)
print(wref)
# <weakref at 0x7f4bdee7c9f8; to 'set' at 0x7f4bdee70c88>

# invoking wref() returns the referenced object, {0, 1}. Because this is a console session; the result {0, 1 is bound to the _variable}
print(wref())
# {0, 1}

# a_set no longer refers to the {0, 1} set, so its reference count is decreased BUT the _ variable still refers to it
a_set ={2, 3, 4}
# calling wref() still returns {0, 1}
print(wref())
# {0, 1}

# when this expression is evaluated, {0, 1} lives, therefore wref() is NOT None. but _ is then bound to the resulting value, False. Now there are no more strong references to {0, 1}
print(wref() is None)
# False

# because the {0, 1} object is now gone, this last call to wref() returns None
print(wref() is None)
# True

'''
consider using WeakKeyDictionary, WeakValueDictionary, WeakSet, and finalize (uses weak references internally) rather than creating and handling your own weakref.ref instances by hand


class WeakValueDictionary 
-implements a mutable mapping where the values are weak references to objects
'''

# example - Cheese has a kind attribute and a standard representation
class Cheese:
    def __init__(self, kind):
        self.kind = kind
    def __repr__(self):
        return 'Cheese(%r)' % self.kind

# example - each cheese loaded from catalog to a stock implemented as WeakValueDictionary; however all but one disappear from the stock as soon as the catalog is deleted

import weakref
# stock is a WeakValueDictionary
stock = weakref.WeakValueDictionary()
catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), 
                Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    # The stock maps the name of the cheese to a weak reference to the cheese instance in the catalog
    stock[cheese.kind] = cheese

print(sorted(stock.keys()))
# the stock is complete
# ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
del catalog
print(sorted(stock.keys()))
# After the catalog is deleted, most cheeses are gone from the stock, as expected, in WeakValueDictionary
# ['Parmesan']
del cheese
print(sorted(stock.keys()))
# []

'''
A counterpart to the WeakValueDictionary is the WeakKeyDictionary in which keys are weak references
weakref module also provides a WeakSet (Set class that keeps weak references to its element)


Limitations of weak references

int and tuples instances CANNOT be targets of weak references, even if subclasses of those types are created
'''
class MyList(list):
    ''' list subcass whose instances may be weakly referenced '''

a_list = MyList(range(10))

# a_list can be the target of a weak reference
wref_to_a_list = weakref.ref(a_list)

'''
Stack Overflow explanation:

each time you create a reference to an object, it is increased by one
each time you delete a reference, it is decreased by one

weak references allow you create references to an object that will NOT increase the reference count

remember that when the refernce count is 0 - garbage will be collected by Python's garbage collector


Tricks Python plays with immutables (optional chapter)
'''
# example - a tuple built from another is actually the SAME exact tuple
t1 = (1, 2, 3)
t2 = tuple(t1)
# t1 and t2 are bound to the SAME object
print(t2 is t1)
# True

t3 = t1[:]
# and so is t3
print(t3 is t1)
# True

# example - String literals may create SHARED objects
t1 = (1, 2, 3)
# creating a new tuple from scratch
t3 = (1, 2, 3)
# t1 and t3 are equal, but not the same object
print(t3 is t1)
# True

s1 = 'ABC'
# creating a second str from scratch
s2 = 'ABC'
# surprise: a and b refer to the same str!
print(s2 is s1)
# True