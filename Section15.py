'''
Context managers and else blocks

Control Flow Features that are NOT common in other languages which is why they are overlooked and underused in Python
    -with statement and context managers
    -else clause in a for, while, and try statements

with statement sets up a temporary context and reliably tears it down, under the control of a context manager object.
*prevents errors and reduces boilerplate code which makes the interface safer and easier to use


Do this, then that: else block beyond if
else clause can be used NOT only in if statements but ALSO for, while, and try statements

for
    else block will run only if and when the for loop runs to completion; i.e not if the for is aborted with a break

while
    else block will run only if and when the while loop exits because the condition became falsy; i.e. not when the while is aborted with a break

try
    else block will only run if NO exception is raised in the try block; "Exceptions in the else clause are NOT handled by the preceding except clauses"

*in ALL cases, else clause is skipped if an exception or a return, break, or continue statement causes control to jump out of the main block of the compound statement
'''
# # example - for/else
# for item in my_list:
#     if item.flavor =='banana':
#         break
# else:
#     raise ValueError('No banana flavor found!')

# example - try/else - more obvious that after_call() will be invoked if there are NO exceptions raised in the try block
# relevant to EAFP (easier to ask forgiveness than permission) coding style and NOT LBYL (look before you leap) coding style
# try:
#     dangerous_call()
#     after_call()
# except OSError:
#     log('OSError...')
# else:
#     after_call()


'''
Context managers and with block

context manager objects exist to control a with statement (just like iterators exist to control a for statement)

with statement is designed to simplify the try/finally pattern which guarantees that some operation is performed after a block of code, even if the block is aborted because of an exception, a return or sys.exit() call

context manager protocol consists of the __enter__ and __exit__ methods
    __enter__ is invoked on the context manager object
    finally clause is played by a call to __exit__ on the context manager object at the end of the with block
'''
# example - demonstration of a file object as a context manager
# # fp is bound to the opened file because the file's __enter__ method returns self
# with open('./Sec15_examples/mirror.py') as fp:
#     # read some data from fp
#     src = fp.read(60)

# print(len(src))
# # 60

# # the fp variable is still available (with blocks DON'T define a new scope like functions and modules do)
# print(fp)
# # <_io.TextIOWrapper name='./Sec15_examples/mirror.py' mode='r' encoding='UTF-8'>

# # you can read the attributes of the fp object
# print(fp.closed, fp.encoding)
# # True UTF-8

# # But you can't perform I/O with fp because at the end of the with block, the TextIOWrapper.__exit__ method is called and closes the file
# print(fp.read(60))
# # Traceback (most recent call last):
# #   File "Section15.py", line 65, in <module>
# #     print(fp.read(60))
# # ValueError: I/O operation on closed file.

'''
the context manager object is the result of evaluating the expression after with, but the value bound to the target variable (in the as clause) is the result of calling __enter__ on the context manager object

the open() function in the example above returns an instance of TextIOWrapper and its __enter__ methods returns self; but the __enter__ method may also return some other object INSTEAD of the context manager

when control flow exits the with block; the __exit__ method is invoked on the context manager object and NOT on whatever is returned by __enter__
'''

# # example - test driving the LookingGlass context manager class
# from Sec15_examples.mirror import LookingGlass

# # The context manager is an instance of LookingGlass; Python calls __enter__ on the context manager and the result is bound to what
# with LookingGlass() as what:
#     # Print a str, then the value of the target variable what
#     print('Alice, Kitty, and Snowdrop')
#     print(what)
# # the output of each print comes out reversed
# # pordwonS dna ,yttiK ,ecilA
# # YKCOWREBBAJ

# # Now the with block is over. We can see that the value returned by __enter__, held in what, is the string 'JABBERWOCKY'
# print(what)
# # JABBERWOCKY

# # Program output is no longer reversed
# print('Back to Normal')
# # Back to Normal

'''
The interpreter calls the __enter__ method with NO arguments - beyond the implicit self. The three arguments passed to __exit__ are:
    exc_type: The exception class ie. ZeroDivisionError

    exc_value: The exception instance. Sometimes, parameters passed to the exception constructor - such as the error message - can be found in exc_value.args

    traceback: A traceback object
'''
# # example - Excersing LookingGlass without a with block so we manually call __enter__ and __exit__ methods
# from Sec15_examples.mirror import LookingGlass

# # # Instantiate and inspect the manager instance
# manager = LookingGlass()
# # print(manager)
# # # <Sec15_examples.mirror.LookingGlass object at 0x7f3261b98780>

# # # Call the context manager __enter__() method and store result in monster
# monster = manager.__enter__()
# # # Monster is the string 'JABBERWOCKY'. The True identifier appears reversed because all output via stdout goes through the write method we patched in __enter__
# print(monster == 'JABBERWOCKY')
# # eurT

# print(monster)
# # YKCOWREBBAJ

# print(manager)
# # >087c867317f7x0 ta tcejbo ssalGgnikooL.rorrim.selpmaxe_51ceS<

# # call manager.__exit__ to restore previous stdout.write
# manager.__exit__(None, None, None)
# print(monster)
# # JABBERWOCKY

'''
contextlib utilities
https://docs.python.org/3/library/contextlib.html

closing
    function to build context managers out of objects that provide a close() method but do NOT implement the __enter__/__exit__ protocol

suppress
    A context manager to temporarily ignore specified exceptions

@contextmanager
    A decorator which lets you build a context manager from a simple generators function, instead of creating a class and implementing the protocol

ContextDecorator
    A base class for defining class-based context managers that can also be used as function decorators, running the entire function within a managed context

ExitStack
    A context manager that lets you enter a variable number of context managers. When the with block ends, ExitStack calls the stacked context managers __exit__ methods in LIFO order. Use this class when you do NOT know beforehand how many context managers you need to enter in your with block. For example, when opening all files from an arbitrary list of files at the same time

**most widely used utility is the @contextmanager decorator


Using @contextmanager

@contextmanager decorator REDUCES the boilerplate of creating a context manager: instead of writing a whole class with __enter__/__exit__ methods, you just simply implement a generator with a single yield that should produce whatever you want the __enter__ method to return

In a generator decorated with @contextmanager, yield is used to SPLIT the body of the function in TWO parts:
    1. everything before the yield will be executed at the beginning of the while block when the interpreter calls __enter__
    2. everything after the yield will run when __exit__ is called at the end of the block
'''

# example - take a look at mirror_gen.py

# example - Test driving the looking_glass context manager function
from Sec15_examples.mirror_gen import looking_glass

# The only difference from the previous example is the name of the context manager: looking_glass instead of LookingGlass
with looking_glass() as what:
    print('Alice, Kitty, and Snowdrop')
    print(what)

# pordwonS dna ,yttiK ,ecilA
# YKCOWREBBAJ

print(what)
# JABBERWOCKY

'''
contextlib.contextmanager decorator wraps the function in a class which implements the __enter__ and __exit__ methods

__enter__ method of that class:
    1. invokes the generator function and holds on to the generator object - let's call it gen
    2. calls next(gen) to make it run to the yield keyword
    3. returns the value yielded by next(gen), so it can be bound to a target variable in the with/as form

when the with block terminates, the __exit__ method of that class:
    1. Checks an exception was passed as exc_type; if so, gen.throw(exception) is invoked, causing the exception to be raised in the yield line inside the generator function body.
    2. Otherwise, next(gen) is called, resuming the execution of the generator function body after the yield

take a look at mirror_gen.py
take a look at mirror_gen_exc.py

*with @contextmanager, the __exit__ method provided by the decorator assumes any exception sent into the generator is handled and should be suppressed (opposite of the __exit__ method WITHOUT @contextmanager)
*Must explicitly re-raise an exception in the decorated function if you don't want @contextmanager to suppress it
'''
# # example - real life example of @contextmanager (Martijn Pieter's in place file rewriting context manager)
# # example - context manager for rewriting files in place
# import csv

# with inplace(csvfilename, 'r', newline='') as (infh, outfh):
#     reader = csv.reader(infh)
#     writer = csv.write(outfh)

#     for row in reader:
#         row += ['new', 'columns']
#         writer.writerow(row)


'''
inplace function is a context manager that gives you two handles - infh and outfh - to the same file which allows your code to read and write to it at the same time

https://www.zopatista.com/python/2013/11/26/inplace-file-rewriting/ (source code)
**everything before the yield keyword is setting up the context which entails creating a backup file then opening and yielding references to the readable and writeable file handles that will be returned by the __enter__ call
**the __exit__ processing after the yield closes the file handles and restores the file from the back up if something went wrong

***use of yield with @contextmanager decorated generator has NOTHING to do with iteration; acts more like a coroutine (procedure that runs up to a point, then suspends to let the client code run until the client wants the coroutine to proceed with its job)
'''