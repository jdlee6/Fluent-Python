# example - spinner_asyncio.py: Animating a text spinner with a coroutine

import asyncio, itertools, sys

# coroutines intended for use with asyncio should be decorated with @asyncio.coroutine. This not mandatory, but is highly advisable. 
@asyncio.coroutine
# here we don't need the signal argument which was used to shut down the thread in the spin function from spinner_thread.py
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # use yield from asyncio.sleep(.1) instead of just time.sleep(.1) to sleep without blocking the event loop
            yield from asyncio.sleep(.1)
        # if asyncio.CancelledError is raised after spin wakes up, it's because cancellation was requested, so exit the loop
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))
    
@asyncio.coroutine
# slow_function is now a coroutine, and uses yield from to let the event loop proceed while this coroutine pretends to do I/O by sleeping
def slow_function():
    ''' pretend waiting a long time for I/O '''
    # the yield from asyncio.sleep(3) expression handles the control flow to the main loop, which will resume this coroutine after the sleep delay
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
# supervisor is now a coroutine as well, so it can drive slow_function with yield from
def supervisor():
    # python3.7 does NOT support asyncio.async --> need to run this script in Python3.6
    # asyncio.async() schedules the spin coroutine to run, wrapping it in a Task object, which is returned immediately
    spinner = asyncio.async(spin('thinking!'))
    # Display the Task object. The output looks like <Task pending coro=<spin() running at spinner_asyncio.py:12>>
    print('spinner object:', spinner)
    # Drive the slow_function(). When that is done, get the returned value. Meanwhile, the event loop will continue running because slow_function ultimately uses yield from asyncio.sleep(3) to hand control back to the main loop
    result = yield from slow_function()
    # A Task object can be cancelled; this raises asyncio.CancelledError at the yield line where the coroutine is currently suspended. The coroutine may catch the exception and delay or even refuse to cancel
    spinner.cancel()
    return result

def main():
    # Get a reference to the event loop
    loop = asyncio.get_event_loop()
    # Drive the supervisor coroutine to completion; the return value of the coroutine is the return value of this call
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)

if __name__ == "__main__":
    main()

'''
the use of the @asyncio.coroutine decorator is NOT mandatory but HIGHLY recommended: it makes the coroutines stand out among regular functions and helps with debugging by issuing a warning when a coroutine is garbage collected without being yielded from - which means some operation was left unfinished and is likely a bug
'''
