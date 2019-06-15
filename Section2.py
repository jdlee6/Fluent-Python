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
# Tuple to receive an expression to unpack can have nested tuples and Python will do the right thing if matches the nesting structure

# metro_area = [
#     ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
#     # Each tuple holds a record with four fields, the last of which is a coordinate pair
#     ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
#     ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
#     ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
#     ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
# ]

# print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
# fmt = '{:15} | {:9.4f} | {:9.4f}'
# by assign the last field to a tuple, we unpack the coordinates
# for name, cc, pop, (latitude, longitude) in metro_area:
    # if longitude <= 0: limits the output to metropolitan areas
    # if longitude <= 0:
        # print(fmt.format(name, latitude, longitude))

'''
'^' forces the field to be centered within the available space
'<' forces the field to be left-aligned within the available space
'>' forces the field to right-aligned within the available space
'''


# Named Tuples
# collections.namedtuple function produces subclasses of tuple with field names and class names

# from collections import namedtuple
# # TWO parameters are required - class name and list of field names 
# City = namedtuple('City', 'name country population coordinates')
# # Data must be passed as positional arguments to constructor
# tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# print(tokyo)
# # City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))

# # able to access the fields by name/position
# print(tokyo.population)
# # 36.933
# print(tokyo.coordinates)
# # (35.689722, 139.691667)
# print(tokyo[1])
# # JP

# ''' 
# few attributes it addition to those inherited from tuple - 
# _fields (class attribute), 
# _make(iterable) (class method)
# _asdict() (instance method)
# '''

# # _fields is a tuple with the field names of the class
# print(City._fields)
# # ('name', 'country', 'population', 'coordinates')
# LatLong = namedtuple('LatLong', 'lat long')
# delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
# # _make( ) lets you instantiate a named tuple from an iterable; City(*delhi_data) would do the same
# delhi = City._make(delhi_data)
# # _asdict( ) returns a collections.OrderedDict built from the named tuple instance which can used to produce a nice display of city data
# print(delhi._asdict())
# # OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935), ('coordinates', LatLong(lat=28.613889, long=77.208889))])
# for key, value in delhi._asdict().items():
#     print(key + ':', value)
# # name: Delhi NCR
# # country: IN
# # population: 21.935
# # coordinates: LatLong(lat=28.613889, long=77.208889)

####################################################################################################

# Tuples as immutable lists
# see Section2.txt

# Slicing - Slice objects
# s[a:b:c] can be used to specify a stride or step c; causing the resulting slice to skip items
# stride c can also be negative which will return items in reverse

# s = 'bicycle'
# print(s[::3])
# bye
# print(s[::-1])
# elcycib
# print(s[::-2])
# eccb

''' Recall the example from our unshuffled deck 
deck[12::13]
[Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'),
Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]
'''
# the notation a:b:c is only valid within [] and produces a slice object: slice(a, b, c)

# Suppose you need to parse flat-file data like the example below 

# invoice = '''
# 0..........6............................................40....................52...55..............
#    1909     Pimoroni PiBrella                 $17.50             3     $52.50
#    1489     6mm Tactile Switch x20            $4.95          2     $9.90
# '''
# SKU = slice(0,6)
# DESCRIPTION = slice(6, 40)
# UNIT_PRICE = slice(40, 52)
# QUANTITY = slice(52, 55)
# ITEM_TOTAL = slice(55, None)
# line_items = invoice.split('\n')[2:]
# # print(line_items)
# for item in line_items:
#     print(item[UNIT_PRICE], item[DESCRIPTION])

    #   $17.50 9     Pimoroni PiBrella           
    #   $4.95  9     6mm Tactile Switch x20


# Multi-dimensional slicing and ellipses
# example: numpy.ndarray can be fetched using a[i, j] and a 2 dimensional slice obtained
# with an expression like a[m:n, k:l]

# example: ellipsis class name is ALL lowercase and the instance built is Ellipsis
# just like bool is ALL lowercase and its instances are True and False
# Numpy uses . . . as a shortcut when slicing arrays of many dimensions
# example: if x is a 4-dimensional array, x[i, . . .] is a short for 
# x[i, :, :, :,]

# Slices can be used to change mutable sequences in place that is without rebuilding them from scratch


# Assigning to slices
# l = list(range(10))
# print(l)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# l[2:5] = [20, 30]
# print(l)
# [0, 1, 20, 30, 5, 6, 7, 8, 9]

# del l[5:7]
# print(l)
# [0, 1, 20, 30, 5, 8, 9]

# l[3::2] = [11, 22]
# print(l)
# [0, 1, 20, 11, 5, 22, 9]

# l[2:5] = 100
# print(l)
# l[2:5] = 100
# TypeError: can only assign an iterable
# when the target of the assignment is a slice, the right hand side must be an iterable object even if it has just one item

# l[2:5] = [100]
# print(l)
# [0, 1, 100, 22, 9]

####################################################################################################

# Using + and * with sequences
# Both + and * always create a new obejct and never change their operands 

# to concatenate multiple copies of the same sequence, multiply it by an integer
# l = [1, 2, 3]
# print(l*5)
# [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]

# print(5*'abcd')
# abcdabcdabcdabcdabcd


# Building lists of lists
# cases where we may need to initialize a list with a certain number of nested lists is to represent squares on a game board or to distribute students in a list of teams

# create a list of with 3 lists of 3 items each. Inspect the structure
# board = [['_'] * 3 for i in range(3)]
# print(board)
# [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# Place a mark in row 1, column 2 and check the result
# board[1][2] = 'X'
# print(board)
# [['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']


''' 
The wrong way to do this would be the following: 
'''
# outer list is made of three references to the same inner list.
# weird_board = [['_'] *3] * 3
# print(weird_board)
# [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']

# placing a mark in row 1 column 2 reveals all rows are aliases referring to the same object
# weird_board[1][2]='O'
# print(weird_board)
# [['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]

''' 
The reason the code above behaves like so is because it behaves like this:
'''
# row = ['_'] * 3
# board = []
# for i in range(3):
#     board.append(row)
    # the same row is appended 3 times to the board

'''
On the other hand, the listcomp is equivalent to:
'''
# board = []
# for i in range(3):
    # row = ['_'] * 3
    # each iteration builds a NEW row and appends it to board
    # board.append(row)

# print(board)
# [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
# board[2][0] = 'X'
# print(board)
# only row 2 is changed as expected
# [['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]


###################################################################################################

# Augmented assignment with sequences

# augmented assignment operators += and *= behave very differently depending on the first operand
# special method that makes += work is __iadd__ ('in-place addition') however if __iadd__ is not implemented, Python
# falls back to calling __add__

# demonstration of *= with a mutable sequence and an immutable one
# l = [1, 2, 3]
# print(id(l))
# # 140160319868872
# # id of the initial list

# l *= 2 
# print(l)
# # [1, 2, 3, 1, 2, 3]
# print(id(l))
# # 140160319868872
# # after multiplication, the list is the SAME object with new items appended

# t = (1, 2, 3)
# print(id(t))
# # 140425845164072
# # id of the intial tuple

# t *= 2 
# print(id(t))
# # 140425865623880
# # after multiplication, a new tuple was created

# # repeated concatenation of immutable sequences is inefficient because instead 
# # of appending new items, the interpreter has to copy the whole target sequence
# # to create a new one with the new items concatenated

###################################################################################################

# dis module shows whats going on in this equation
# import dis
# print(dis.dis('s[a] += b'))
# first load_name, s, and then load name, a. 
# then we duplicate the two references of top of the slack, leaving them in order
# then we implement TOS = TOS1[TOS] (Puts value of s[a] on Top of Stack)
# then we load_name, b
# then it implements in-place TOS = TOS1 + TOS or TOS += b (succeeds if TOS refers to a mutable object)
# then it lists second and third stack item one position up, move top down to position 3
# then implements TOS1[TOS] = TOS2 or Assigns s[a] = TOS (fails if s is immutable)
# then we push co_consts[consti] onto the stack
# and then we return the value
'''
  1           0 LOAD_NAME                0 (s)
              2 LOAD_NAME                1 (a)
              4 DUP_TOP_TWO
              6 BINARY_SUBSCR
              8 LOAD_NAME                2 (b)
             10 INPLACE_ADD
             12 ROT_THREE
             14 STORE_SUBSCR
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
'''

###################################################################################################

# list.sort and the sorted built-in function

# list.sort - sorts a list without making a copy
# sorted function creates a new list and returns it
# both take two optional, keyword-only arguments: key and reverse

# fruits = ['grape', 'raspberry', 'apple', 'banana']

# # produces a new list of strings sorted alphabetically
# print(sorted(fruits))
# # ['apple', 'banana', 'grape', 'raspberry']

# # inspecting the original list to see that it is unchanged
# print(fruits)
# # ['grape', 'raspberry', 'apple', 'banana']

# # this is reverse alphabetical ordering
# print(sorted(fruits, reverse=True))
# # ['raspberry', 'grape', 'banana', 'apple']

# # new list of strings sorted by length (original order for grape and apple because both have a length of 5)
# print(sorted(fruits, key=len))
# # ['grape', 'apple', 'banana', 'raspberry']

# # these are strings sorted in descending order of length
# print(sorted(fruits, key=len, reverse=True))
# # ['raspberry', 'banana', 'grape', 'apple']

# # sorts the list in-place and returns None (console doesnt show)
# fruits.sort()
# print(fruits)
# # ['apple', 'banana', 'grape', 'raspberry']

###################################################################################################

# Managing ordered sequences with bisect
# bisect module offers TWO functions (bisect and insort)

# Searching with bisect
# bisect(haystack, needle) - searches for needle in haystack (sorted sequence)

# import bisect, sys

# HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
# NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

# ROW_FMT = '{0:2d} @ {1:2d}    {2}{0:<2d}'

# def demo(bisect_fn):
#     for needle in reversed(NEEDLES):
#         # use the chosen bisect function to get the insertion point
#         position = bisect_fn(HAYSTACK, needle)
#         # build a pattern of vertical bars proportional to the offset
#         offset = position * '  |'
#         # print formatted row showing needle and insertion point
#         print(ROW_FMT.format(needle, position, offset))

# if __name__ == "__main__":
#     # choose the bisect function to use according to the last command line argument
#     if sys.argv[-1] == 'left':
#         bisect_fn = bisect.bisect_left
#     else:
#         bisect_fn = bisect.bisect
# # print header with name of function selected
# print('Demo: ', bisect_fn.__name__)
# print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))

# demo(bisect_fn)

# Each row starts with the notation needle @ position and the needle value appears again below its insertion point in the haystack
# Behavior of bisect can be fine tuned in two ways
# 1. pair of optional arguments lo and hi
# 2. bisect is an alias for bisect_right and there is a sister function called bisect_left
# bisect_right returns an insertion point AFTER the existing item and the bisect_left 
# returns the position of the existing item BEFORE


''' 
Perform table lookups by numeric values,
for example: convert test scores to letter grades 
'''
# import bisect

# def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
#     i = bisect.bisect(breakpoints, score)
#     return grades[i]

# print([
#     grade(score) for score in [33, 99, 77, 70, 89, 90, 100]
# ])

# ['F', 'A', 'C', 'C', 'B', 'A', 'A']


# Inserting with bisect.insort
# insort(seq, item) inserts item into seq so as to keep seq in ascending order

# Seeding a pseudo random number generator gives it its first "previous" value
# if you provide the same seed twice, you get the SAME sequence of number twice

# random.seed(1729)
# print(random.random(), random.random())
# 0.9963723767827669 0.8848200965298146

# random.seed(1729)
# print(random.random(), random.random())
# 0.9963723767827669 0.8848200965298146

# import bisect, random

# SIZE = 7
# random.seed(1729)

# my_list = []
# for i in range(SIZE):
#     new_item = random.randrange(SIZE * 2)
#     bisect.insort(my_list, new_item)
#     print('%2d ->' % new_item, my_list)

# 10 -> [10]
#  0 -> [0, 10]
#  6 -> [0, 6, 10]
#  8 -> [0, 6, 8, 10]
#  7 -> [0, 6, 7, 8, 10]
#  2 -> [0, 2, 6, 7, 8, 10]
# 10 -> [0, 2, 6, 7, 8, 10, 10]