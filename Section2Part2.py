''' 
Part 2 because Section2.py was getting too long
Focuses on handling lists of numbers (arrays) 

Mutable sequence types that can REPLACE lists
in many cases, starting with arrays
'''

# Arrays

# If ALL you want to put in the list are NUMBERS, array.array is more efficient than a list
# includes .pop, .insert, .extend // .frombytes and .tofile

# # import array type
# from array import array
# from random import random

# # create an array of double-precision floats (typecode 'd') from any iterable object
# # in this case a generator expression
# # 10,000,000 numbers
# floats = array('d', (random() for i in range(10**7)))

# # print the last number in the array
# print(floats[-1])

# # save the array to a binary file
# fp = open('floats.bin', 'wb')
# floats.tofile(fp)
# fp.close()

# # create an empty array of doubles
# floats2 = array('d')
# fp = open('floats.bin', 'rb')
# # read 10 million numbers from the binary file
# floats2.fromfile(fp, 10**7)
# fp.close()
# # inspect last number of array
# print(floats2[-1])

# # verify that the contents of the array match
# print(floats2 == floats)

# notice the quickness - ~0.1s for array.fromfile to load 10 million double precision floats from a binary file created with array.tofile
# size of binary file with 10 million doubles is 80,000,000 bytes whereas a textfile has 181,515,739 bytes for the same data

'''
array type does not have an in-place sort method like list.sort( )
if you need to sort an array, use the sorted function to rebuild it sorted:
a = array.array(a.typecode, sorted(a))
'''
# to keep a sorted array sorted while adding items to it, use the bisect.insort function 

###################################################################################################

# Memory Views
