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

# memoryview allows you to share memory between data structures without first copying (important for large data sets)

# import array
# numbers = array.array('h', [-2, -1, 0, 1, 2])
# # build memoryview from array of 5 short signed integers (typecode 'h')
# memv = memoryview(numbers)

# print(len(memv))
# # 5
# # memv sees the same 5 items in the array
# print(memv[0])
# # -2

# # create memv_oct by casting the elements of memv to typecode 'B' (unsigned char)
# # memoryview.cast method lets you change the way multiple bytes are read or written as units without moving bits around
# # return value is a new memory view but the buffer is not copied
# memv_oct = memv.cast('B')
# print(memv_oct.tolist())
# # [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]

# # assign value 4 to byte offset 5
# # byte offset is the count of bytes starting at 0
# memv_oct[5] = 4
# print(memv_oct.tolist())
# # [254, 255, 255, 255, 0, 4, 1, 0, 2, 0]

# # unsigned integer can hold a larger positive value and NO negative value
# # unsigned uses the leading bit as apart of the value while the signed version uses the left most bit to identify
# # if the number is positive or negative
# # signed integers can hold both postiev and negative numbers

# # byteorder detemines the byte order used to represent the integer
# # if byteorder = "big", the most significant byte is at the beginning of the byte array
# # if byteorder="little", the most significant byte is at the end of the byte array

# '''
# ******
# '''
# # note change to numbers variable: a 4 in the most significant byte of a 2-byte unsigned integer is 1024
# print(numbers)
# # array('h', [-2, -1, 1024, 1, 2])

###################################################################################################

# NumPy and SciPy

# # import Numpy
# import numpy

# # build and inspect a numpy.ndarray with integers 0 to 11
# a = numpy.arange(12)
# print(a)
# # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# print(type(a))
# # <class 'numpy.ndarray'>

# # inspect the dimensions of the array: this is a one-dimensional, 12-element array
# print(a.shape)
# # (12,)

# # change the shape of the array, adding one dimension then inspect the results
# a.shape = 3, 4
# print(a)
# # [[ 0  1  2  3]
# #  [ 4  5  6  7]
# #  [ 8  9 10 11]]

# # get row at index 2
# print(a[2])
# # [ 8  9 10 11]

# # get element at index 2, 1
# print(a[2, 1])
# # 9

# # get column at index 1
# # [:,] grabs all values from column at index 1
# print(a[:, 1])
# # [1 5 9]
# print(a[1:, 1]) 
# # [5, 9]

# # creates a new array by transposing (swapping columns with rows)
# print(a.transpose())
# # [[ 0  4  8]
# #  [ 1  5  9]
# #  [ 2  6 10]
# #  [ 3  7 11]]

''' 
Loading, Saving, Operating on all elements of a numpy.ndarray 
'''
# from time import perf_counter as pc
# import time

# print(pc())
# print(time.time())

# import numpy

# # loads 10 million floating point numbers from a text file
# floats = numpy.loadtxt('floats-10M-lines.txt')

# # use sequence slicing notation to inspect the last 3 numbers
# print(floats[-3:])
# # array([ 3016362.69195522, 535281.10514262, 4566560.44373946])

# # multiply every element in the floats array by .5 and inspect last 3 elements again;
# floats*=.5
# print(floats[-3:])
# # array([ 1508181.34597761, 267640.55257131, 2283280.22186973])

# # import the high resolution perormance measure timer
# # mainly used to  evaluate relative performance (whether this version of code runs faster than that version of code)
# from time import perf_counter as pc

# # divide every element by 3; the elapsed time for 10 million floats is less than 4 seconds
# # different lines of code in one line which is separated by the ;
# t0 = pc(); floats /= 3; pc() - t0
# print(t0)
# # 0.03690556302899495

# # save the array in a .npy binary file
# numpy.save('floats-10M', floats)

# # load the data as a memory-mapped file into another array; this allows efficient processing of slices of the array even if it does not fit entirely in memory
# # r+
# floats2 = numpy.load('floats-10M.npy', 'r+')

# # inspect the last 3 elements after multiplying every element by 6
# floats2 *= 6
# print(floats2[-3:])
# # memmap([ 3016362.69195522, 535281.10514262, 4566560.44373946])
###################################################################################################

# Deques and other queues

# collections.deque - fast inserting and removing from both ends
# used for "last seen items" and such

# from collections import deque

# # the optional maxlen argument set the maximum number of items 
# # allowed in this instance of deque; this sets a read-only maxlen instance attribute
# dq = deque(range(10), maxlen=10)
# print(dq)
# # deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

# # rotating with n > 0 takes items from the right end and prepends them
# # to the left; when n < 0 items are taken from left and appended to the right
# dq.rotate(3)
# print(dq)
# # deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)

# dq.rotate(-4)
# print(dq)
# # deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)

# # appending to a deque that is full (len(d) == d.maxlen) discards items from the other end; 
# # note in the next line that 0 is dropped
# dq.appendleft(-1)
# # deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
# print(dq)

# # adding three items to the right pushes out the left most -1, 1, 2
# dq.extend([11, 22, 33])
# print(dq)
# # deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)

# # note that extendleft(iter) works by appending each successive item of the iter argument
# # to the left of the deque, therefore the final position of the items is reversed
# dq.extendleft([10, 20, 30, 40])
# print(dq)
# # deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)

'''
Other Python Standard Library packages implement queues
- queue
- multiprocessing
- asyncio 
- heapq
'''
