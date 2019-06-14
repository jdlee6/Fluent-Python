''' An Array of Sequences '''

# List comprehensions is a powerful way of building lists which is soemwhat underused because the syntax may be unfamiliar
# Mastering list comprehensions opens the door to generator expressions, which can produce elements to fill up sequences of any type

''' List comprehensions and generator expressions '''
# numbers = [1, 2, 3, 4, 5, 6, 7, 8,]

# default standard
# number_list = []
# for number in numbers:
#     number_list.append(number)
# print(number_list)

# list comp (this is more readable because the intent is explicit)
# number_list_two = [
#     number for number in numbers
# ]
# print(number_list_two)

# the code in the first example is building up a list whereas the listcomp is meant to do one thing only: to build a list
# don't use listcomps if you don't intend to do something with that produced list
# if list comp spans more than 2 lines, it's probably better using the regular for loop

####################################################################################################

# Listcomps vs. map and filter
# ord( ) returns the integer of the byte when the argument is an 8 bit string
# lambda are functions with no names - small anonymous functions usually not more than one line
# symbols = '$¢£¥€¤'
# beyond_ascii = [
#     ord(s) for s in symbols if ord(s) > 127
# ]
# print(beyond_ascii)

# map and filter method (will be discussed in chapter 5)
# symbols = '$¢£¥€¤'
# beyond_ascii_two = list(filter(lambda c: c > 127, map(ord, symbols)))
# print(beyond_ascii_two)

####################################################################################################

# Cartesian products
# 2 lists
# items that make up the cartesian product are tuples made from items from every input iterable
# the resulting list has a length equal to the lengths of the input iterables multiplied

''' imagine you need to produce a list of tshirts available in two colors and three sizes '''

# colors = ['black', 'white']
# sizes = ['S', 'M', 'L']

# this generates a list of tuples arranged by color then size
# [('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'), ('white', 'M'), ('white', 'L')]
# tshirts = [
#     (color, size) for color in colors for size in sizes
# ]
# print(tshirts)

# The resulting list is arranged as if the for loops were nested in the same order as they appear in the listcomp
# for color in colors:
#     for size in sizes:
#         print((color, size))

# to get items arranged by size, then color, just rearrange the for clauses; adding a line break to the list comp makes it easy to see how the result will be ordered
# [('black', 'S'), ('white', 'S'), ('black', 'M'), ('white', 'M'), ('black', 'L'), ('white', 'L')]
# tshirts_two = [(color, size) for size in sizes 
#                                             for color in colors]
# print(tshirts_two)

# listcomps are only used to build lists. To fill up other sequence types; a genexp is the way to go

####################################################################################################

# Generator expressions

# to initialize tuples, arrays and other types of sequences - you COULD also start from a listcomp but a genexp saves memory because it yields items one by one using the iterator protocol INSTEAD of building a whole list just to feed another constructor

# Genexps use the same syntax as listcomps but are enclosed in parenthesis rather than brackets
# note if you dont have the tuple( ) method it will return a generator object like so: <generator object <genexpr> at 0x7fcbfb1984f8>
# symbols = '$¢£¥€¤'

# if the generator expression is the single argument in a function call, there is NO need to duplicate the enclosing parenthesis
# exp = tuple(
#     ord(symbol) for symbol in symbols
# )
# print(exp)

# the array constructors takes two arguments, so the parenthesis around the generator expressions are MANDATORY
# import array
# exp_two = array.array('I', (ord(symbol) for symbol in symbols))
# print(exp_two)


# Cartesian product in a generator expression
''' Listcomp we used for tshirts and colors above is NEVER built in memeory
the generator expression feeds the for loop producing one item at a time 

example: if we had two lists of 1000 items each; using a generator expression would save
the expense of building a list with a million items just to feed the for loop''' 
# colors = ['black', 'white']
# sizes = ['S', 'M', 'L']

# notice the f string conversion from %s
# the generator expression yields items one by one; a list with all 6 tshirt variations is NEVER produced in this example
# for tshirt in (f'{c} {s}' for c in colors for s in sizes):
#     print(tshirt)

# black L
# white S
# white M
# white L

# for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
#     print(tshirt)

####################################################################################################

# Tuples can be used as immutable lists and also as records with no field names

# Tuples as records
# when using a tuple as collection of fields, the number of items is often fixed and their order is VITAL
# in the examples below, SORTING the tuple will destroy the information because the meaning of each data is given by its position in the tuple

lax_coordinates = (33.94, -118.40)
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
    
# f strings can not split tuples
# % formatting operator understands tuples and treats each item as a separate field
# for passport in sorted(traveler_ids):
    # print(f'{passport/passport}')
    # print('%s/%s' % passport)

# the for loop knows how to retrieve the items of a tuple separately - this is called "unpacking"
# the _ is a dummy variable 
# for country, _ in traveler_ids:
#     print(country)

# Tuple unpacking
'''
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)

for passport in sorted(traveler_ids):
    print('%s/%s' % passport)

These are two examples of Tuple unpacking'''

# parallel assignment (swapping the values of variables without using a temporary variable)
# lax_coordinates = (33.94, -118.40)
# latitude, longitude = lax_coordinates 
# print(latitude, longitude)

# another example is prefixing an argument with a star when calling a function
# x is the numerator, and y is the denominator in a divmod function
# 8 goes into 20, TWO times and is left with a remainder of FOUR
# print(divmod(20, 8))
# (2, 4)

# t = (20, 8)
# print(divmod(*t))
# (2, 4)

# quotient, remainder = divmod(*t)
# print(quotient, remainder)
# 2 4

# os.path.split( ) function builds a tuple of (path, last_part) so ...
# import os
# _, filename = os.path.split('/home/joe/Documents/ATBSch1.docx')
# print(filename)
# ATBSch1.docx

####################################################################################################

# Using * to grab excess items

# Defining function parameteres with *args to grab arbitray excess arguments is a classic Python feature

# a, b, *rest = range(5)
# print(a, b)
# print(a, b, rest)
# 0 1
# 0 1 [2 3 4]
# rest in this case refers to 2 3 4 

# a, b, *rest = range(3)
# print(a, b)
# print(rest)
# 0 1
# [2]

# a, b, *rest = range(2)
# print(a, b)
# print(rest)
# 0 1
# []

''' In the context of parallel assignment, the *prefix can be applied to exactly one variable but it can appear in any position '''
# a, *body, c, d = range(5)
# print(a, c, d)
# print(body)
# 0 3 4
# [1, 2]

# *head, b, c, d = range(5)
# print(head)
# print(b, c, d)
# [0, 1]
# 2 3 4

####################################################################################################

# Nested Tuple Unpacking
