# example - use of try/finally to perform actions on coroutine termination

class DemoException(Exception):
    ''' an exception type for the demonstration '''

def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing . . .')
            else: 
                print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')