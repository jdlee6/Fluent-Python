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

# # adding an item to lewish is the same as adding an item to charles
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

if the referenced items are mutable; the may change if the tuple itself does NOT
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

# example - defines class Bus, represeting a school bus that is loaded with passengers and then picks or drops passengers on its route

class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

# example continued - effects of using copy vs. deepcopy
import copy

bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)

# using copy and deepcopy, we create three distinct Bus instances
print(id(bus1), id(bus2), id(bus3))
# 140544378607432 140544378607656 140544378608552

bus1.drop('Bill')
# after bus1 drops 'Bill', he is also missing from bus2
print(bus2.passengers)
# ['Alice', 'Claire', 'David']

# inspection of the passengers attribute shows that bus1 and bus2 share the SAME list object, because bus2 is a SHALLOW copy of bus1
print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
# 140063737346952 140063737346952 140063737232648

#bus3 is a deep copy of bus1, so its passengers attribute refers to another list
print(bus3.passengers)
# ['Alice', 'Bill', 'Claire', 'David']
