# example - simple demonstration of the map method of ThreadPoolExecutor

from time import sleep, strftime
from concurrent import futures

# this function simply prints whatever argument it gets, preceded by a timestamp in the format [HH:MM:SS]
def display(*args):
    print(strftime('[%H:%M:%S]'), end='')
    print(*args)

# loiter does nothing except display a message when it starts, sleep for n seconds, then display a message when it ends; tabs are used to indent the message according to the value of n
def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s'
    display(msg.format('\t' *n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    # loiter returns n*10 so we can see how to collect results
    return n * 10

def main():
    display('Script starting.')
    # Create a ThreadPoolExecutor with 3 threads
    executor = futures.ThreadPoolExecutor(max_workers=3)
    # Submit 5 tasks to the executor; because there are only 3 threads, ONLY three of those tasks will start immediately: the calls loiter(0), loiter(1), and loiter(2); this is a non-blocking call
    results = executor.map(loiter, range(5))
    # immediately display the results of invoking executor.map: it's a generator, as the output below
    display('results:', results)
    display('Waiting for individual results:')
    # The enumerate call in the for loop will implicitly invoke next(results), which in turn will invoke _f.result() on the (internal) _f future representing the first call, loiter(0). The result method will block until the future is done, therefore each iteration in this loop will hae to wait for the next result to be ready
    for i, result in enumerate(results):
        display('result {}:{}'.format(i, result))

main()


''' output '''
# This run started at 17:23:12
# [17:23:12]Script starting.

# The first thread executes loiter(0), so it will sleep for 0s and return even before the second thread has a chance to start, but YMMV
# [17:23:12]loiter(0): doing nothing for 0s
# [17:23:12]loiter(0): done.

# loiter(1) and loiter(2) start immediately (since the thread pool has 3 workers, it can run 3 functions concurrently)
# [17:23:12]      loiter(1): doing nothing for 1s
# [17:23:12]              loiter(2): doing nothing for 2s

# this shows that results returned by executor.map is a generator; nothing so far would block, regardless of the number of tasks and the max_workers setting
# [17:23:12]results: <generator object Executor.map.<locals>.result_iterator at 0x7f1163c36138>

# Because loiter(0) is done, the first worker is now available to start the fourth thread for loiter(3)
# [17:23:12]                      loiter(3): doing nothing for 3s
# [17:23:12]Waiting for individual results:

# This is where execution may block, depending on the parameters given to the loiter calls: the __next__ method of the results generator MUST wait until the first future is complete. In this case it won't block because the call to loiter(0) is finished before this loop started. Note that everything up to this point happened within the same second: 17:23:12
# [17:23:12]result 0:0

# loiter(1) is done one second later, at 17:23:13. The thread is freed to start loiter(4)
# [17:23:13]      loiter(1): done.
# [17:23:13]                              loiter(4): doing nothing for 4s

# The result of loiter(1) is shown: 10. Now the for loop will block waiting for the result of loiter(2)
# [17:23:13]result 1:10

# The pattern repeats: loiter(2) is done, it's result is shown; same with loiter(3)
# [17:23:14]              loiter(2): done.
# [17:23:14]result 2:20
# [17:23:15]                      loiter(3): done.
# [17:23:15]result 3:30

# There is a 2s delay until loiter(4) is done, because it started at 17:23:13 and did nothing for 4s
# [17:23:17]                              loiter(4): done.
# [17:23:17]result 4:40