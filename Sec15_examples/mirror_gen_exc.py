# example - mirror_gen_exc.py: generator based context manager implementing exception handling - same external behavior as mirror_gen.py
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    
    sys.stdout.write = reverse_write
    # Create a variable for a possible error message; this is the first change in relation to mirror_gen.py
    msg = ''
    try:
        yield 'JABBERWOCKY'
    # Handle ZeroDivisionError by setting an error message
    except ZeroDivisionError:
        msg = 'Please Do NOT Divide By Zero!'
    finally:
        # Undo monkey-patching of sys.stdout.write
        sys.stdout.write = original_write
        if msg:
            # Display error message, if it was set
            print(msg)

            