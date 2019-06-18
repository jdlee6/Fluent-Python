'''
Functions are first class objects
1. created @ runtime
2. assigned to a variable or element in a data structure
3. passed as an argument to a function
4. returned as the result of a function

Treating a function like an object: look at the example below
'''
# create a function in "run time"
# def factorial(n):
#     '''
#     returns n
#     '''
#     # ternary conditional 
#     return 1 if n <2 else n * factorial(n-1)

# print(factorial(5))
# # 120

# # __doc__ is one of several attributes of function objects
# # used to generate the help text of an object
# print(factorial.__doc__)

#     # returns n

# # factorial is an instance of the function class    
# print(type(factorial))
# # <class 'function'>

# # We can assign the function above a variable and call it through that name
# # We can also pass factorial as an argument to map 
# # map function returns an iterable where each item is the result of the application of the first argument (function) to successive elements of the second argument (iterable)

# fact = factorial
# print(fact)
# # <function factorial at 0x7f08c085f1e0>

# print(fact(5))
# # 120

# print(map(factorial, range(11)))
# # <map object at 0x7f4513133780>

# print(list(map(fact, range(11))))
# # [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

###############################################################################


'''
Higher-order functions

function that takes a function as an argument or returns a function as result is a higher-order function
ie. map(), sorted() - optional keyword - sort - is a function
'''
# # Sorting a list of words by length
# fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# # function here is the len argument
# print(sorted(fruits, key=len))
# # ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']

# # Sorting a list of words by their reversed spelling
# def reverse(word):
#     return word[::-1]
# print(reverse('testing'))
# # gnitset
# print(sorted(fruits, key=reverse))
# # ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

###############################################################################


'''
Modern replacements for map, filter, reduce

map and filter functions are built in functions - returns generators (a form of an iterator)
listcomp / genexp does the job of both and is MORE readable
'''
# # build a list of factorials from 0! to 5!
# print(list(map(fact, range(6))))
# # [1, 1, 2, 6, 24, 120]

# # same operation with a list comprehension
# print([
#     fact(n) for n in range(6)
# ])
# # [1, 1, 2, 6, 24, 120]

# # list of factorials of odd numbers upto 5! using both map and filter
# print(list(map(factorial, filter(lambda n: n%2, range(6)))))
# # [1, 6, 120]

# # list comprehensions do the same job (replaces map and filter which make lambda unnecessary)
# print([
#     factorial(n) for n in range(6) if n % 2
# ])
# # [1, 6, 120]

'''
Example - sum of integers up to 99 performed with reduce and sum

all(iterable) - True if every element of iterable is truthy
any(iterable) - True if any element of iterable is truthy

to use a higher order function, sometimes it is convenient to create a small, one off function
'''


# # reduce is not a built in function anymore (after Python3)
# from functools import reduce
# # import add to avoid creating a function just to add two numbers
# from operator import add

# # sum integers up to 99
# print(reduce(add, range(100)))
# # 4950

# # same task; import or adding function NOT needed
# print(sum(range(100)))
# # 4950


###############################################################################


''' 
Anonymous functions

lambda keyword creates an anonymous function within a Python expression
- body of a lambda CANNOT make assignments or use any other Python statement (while, try, etc...)
    
if hard to read:
    1. write a comment explaining what that lambda does
    2. study the comment
    3. convert to a def statement 
    4. remove comment
'''

# # example - sorting a list of words by their reversed spelling using lambda
# fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# # lambda is taking the single argument word and then returning word[::-1]
# print(sorted(fruits, key=lambda word: word[::-1]))
# # ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

###############################################################################


'''
Seven flavors of callable objects
- to determine whether an object is callable (use callable())

user-defined functions - def statements or lambda
built-in functions - len or time.strftime
built-in methods - dict.get
methods - functions defined in a class
Class - calling a class is like calling a function
Class Instances - if class has __call__ then callable
Generator functions - functions or methods that use the yield keyword (generator functions return a generator object)
'''

