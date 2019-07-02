# example - a context manager implemented with a generator
import contextlib

# apply the contextmanager decorator
@contextlib.contextmanager
def looking_glass():
    import sys
    # preserve original sys.stdout.write method
    original_write = sys.stdout.write

    # define custom reverse_write function; original_write will be available in the closure
    def reverse_write(text):
        original_write(text[::-1])
    
    # replace sys.stdout.write with reverse_write
    sys.stdout.write = reverse_write
    # yield the value that will be bound to the target variable in the as clause of the with statement. This function pauses at this point while the body of the with executes
    yield 'JABBERWOCKY'
    # when control exits the with block in any way, execution continues after the yield; here the original sys.stdout.write is restored
    sys.stdout.write = original_write


'''
*SERIOUS FLAW: if an exception is raised in the body of the with block, the Python interpreter will catch it and raise it again in the yield expression inside looking_glass but because there is NO error handling, looking_glass function will abort without ever restoring the original sys.stdout.write method (leaves the system in an invalid state)

take a look at mirror_gen_exc.py
'''
