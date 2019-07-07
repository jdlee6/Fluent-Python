# example - spinner_thread.py: Animating a text spinner with a thread

import threading, itertools, time, sys

# This class defines a simple mutable object with a go attribute we'll use to control the thread from outside
class Signal:
    go = True

# This function will run in a separate thread. The signal argument is an instance of the Signal class just defined
def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    # This is actually an infinite loop because "itertools.cycle()" produces items cycling from the given sequence forever
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        # The trick to do text-mode animation: move the cursor back with backspace characters (\x08)
        # this restarts the line from the beginning so when "write(status)" is iterated over again, the symbol seems like it just updated.
        write('\x08' * len(status))
        # print('debug-print\n')
        time.sleep(.1)
        # If the go attribute is no longer True, exit the loop
        if not signal.go:
            break
    # Clear the status line by overwriting with spaces and moving the cursor back to the beginning
    write(' ' * len(status) + '\x08' * len(status))
    
# Imagine this is some costly computation
def slow_function():
    ''' pretend waiting a long time for I/O '''
    # calling sleep will block the main thread but, crucially, the GIL will be released so the secondary thread will proceed
    time.sleep(3)
    return 42

# this function sets up the secondary thread, displays the thread object, runs the slow computation and kills the thread
def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking!', signal))
    # display the secondary thread object. The output looks like <Thread(Thread-1, initial)>
    print('spinner object:', spinner)
    # start the secondary thread
    spinner.start()
    # run slow_function(); this blocks the main thread. Meanwhile, the spinner is animated by the secondary thread
    result = slow_function()
    # change the state of the signal; this will terminate the for loop inside the spin function
    signal.go = False
    # wait until the spinner thread finishes
    spinner.join()
    return result

def main():
    # run the supervisor function
    result = supervisor()
    print('Answer:', result)

if __name__ == "__main__":
    main()

'''
when the main thread sets signal.go attribute to false, the spinner thread will eventually notice and exit cleanly
'''
