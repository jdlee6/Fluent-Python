# example - test code for studying exception handling in a coroutine

class DemoException(Exception):
    ''' An exception type for the demonstration '''

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        # Special handling for DemoException
        except DemoException:
            print('*** DemoException handled. Continuing . . .')
        # If no exception, display received value
        else:
            print('-> coroutine received: {!r}'.format(x))
    # This line will never be executed
    raise RuntimeError('This line should never run.')