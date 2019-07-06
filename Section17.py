'''
Concurrency with futures 

"futures" - objects representing the asynchronous execution of an operation


Example: Web downloads in three styles

1. runs sequentially: it only requests the next image when the previous one is downloaded and saved to disk 
2 & 3. make concurrent downloads: they request all images practically at the same time and save the files as they arrive
*flags.py
*flags_threadpool.py uses concurrent.futures package
*flags_asyncio.py uses asyncio

Video demo:
https://www.youtube.com/watch?v=A9e9Cy1UkME

flags.py - the output for each run starts with the country codes of the flags as they are downloaded and ends with a message stating the elapsed time
    took about 8 seconds to download 20 images

flags_threadpool.py - took about 1.4 seconds

flags_asyncio.py - took about 1.35 seconds
    * the order of the country codes: the downloads happened in a different order every time with the concurrent strips

Concurrent scripts are FIVE times more faster than the sequential script (image if you need to download 500+ images sequentially vs concurrently)


A sequential download script
*take a look at flags.py


Downloading with concurrent.futures

ThreadPoolExecutor class and ProcessPoolExecutor class
    implement an interface that allows you to submit callables for execution in different threads or processes, respectively
    the classes manage an internal pool of worker threads or processes, and a queue of tasks to be executed
*take a look at flags_threadpool.py
    *Executor.map: returns an iterator in which __next__ calls the result method of each future, so what we get are the results of the futures and NOT the futures themselves


Where are the futures?

Futures are essential components in the internals of concurrent.futures and of asyncio and they operate more "behind the scenes" in flags_threadpool.py

There are two classes named Future in the standard library: 
    concurrent.futures.Future 
    asyncio.Future
    **both share the same purpose: an instance of either Future class represents a deferred computation that may or may not have completed

Futures encapsulate pending operations so that they can be put in queues, their state of completion can be queried and their results (or exceptions) can be retrieved when available

**Users should NOT be creating Futures; only meant to be instantiated exclusively by either of the concurrency framework 
**Client code is NOT supposed to change the state of a future: the concurrency framework changes the state of a future when the computation it represents is done, and we can't control when that happens

.done() method - non-blocking and returns a boolean that tells you whether the callable linked to that future has executed or not
.add_done_callback() method - give it a callable and the callable will be invoked with the future as the single argument when the future is done
.result() - returns the result of the callable, or re-raises whatever exception might have been thrown when the callable was executed 
    **if not done: behavior is different in concurrent.futures.Future and asyncio.Future
            1. In a concurrent.futures.Future instance,invoking f.result() will BLOCK the caller's thread until the result is ready; optional timeout argument and if the future is NOT done in the specified time --> TimeoutError
            2. asyncio.Future.result method does NOT support timeout, and the way to get the result of futures in that library is to use "yield from" (yield from does NOT work with concurrent.futures.Future instances)

take a look at flags_threadpool_ac.py
    concurrent.futures.as_completed() takes an iterable of futures and returns an iterator that yields futures as they are done
    the Executor.map call is replaced by TWO for loops: 
        1. one to create and schedule the futures
        2. the other to retrieve their results


Blocking the I/O and the GIL
GIL: Global Interpreter Lock (allows only one thread at a time to execute Python bytecodes)
    *single process CANNOT use multiple CPU cores at the same time

all standard library functions that perform blocking I/O, release the GIL when waiting for a result from the OS 


Launching processes with concurrent.futures
package enables truly parallel computations because it supports distributing work among multiple Python processes using the ProcessPoolExecutor class which ends up bypassing the GIL and leveraging all available CPU cores

*BOTH ProcessPoolExecutor and ThreadPoolExecutor implement the generic Executor interface
look at the example below
'''
# # no advantage but to make the change jsut do the following:
# def download_many(cc_list):
#     workers = min(MAX_WORKERS, len(cc_list))
#     with futures.ThreadPoolExecutor(workers) as executor:

# # to

# def download_many(cc_list):
#     with futures.ProcessPoolExecutor() as executor:

# import os
# print(os.cpu_count())

'''
the only notable difference is that ThreadPoolExecutor.__init__ requires a "max_workers" argument which is an OPTIONAL argument in ProcessPoolExecutor (default is the number of CPUs returned by "os.cpu_count()")
    would NOT make sense to ask for MORE workers than CPUs (ProcessPoolExecutor)
    # of threads does NOT matter for ThreadPoolExecutor: you can use 10, 50, 1000 threads
        *finding the optimal number will require careful testing

**avg time to download 20 flags increased to 1.8s with ProcessPoolExecutor - compared to 1.4s in the original ThreadPoolExecutor version
    -the cause is likely to be the limit of the 4 concurrent downloads on a 4-core machine against 20 workers in the threadpool version

**take a look at figure 17-1 on page 544 for other test results
    *PyPy library for CPU-Intensive work


Experimenting with Executor.map
Simplest way to run several callables concurrently is with the Executor.map function we first saw in flags_threadpool.py
'''

# take a look at demo_executor_map.py

'''
The Executor.map function returns the results EXACTLY in the same order as the calls are started: if the first call takes 10s to produce a result, and the other take 1s each, your code will BLOCK for 10s as it tries to retrieve the FIRST result of the generator returned by "map"
    -After this; the remaining results will be obtained without blockage

**Often preferable to get the results as they are ready REGARDLESS of the order they were submitted.
    -To do this: we must use executor.submit() method and futures.as_completed() function like in flagpools_threadpool_ac.py
    **This is MORE FLEXIBLE than executor.map() because you can submit different callables and arguments, while executor.map is designed to run the same callable on the different arguments


Downloads with progress display and error handling
In order to test the handling of a variety of error conditions - we will take a look at flags2_  . . . examples as the flags_ . . . do NOT cover any error handling
    flags2_common.py: module contains common functions and settings used by all flags2 examples, including a main function which takes care of command line parsing, timing and reporting results. <Support Code>

    flags2_sequential.py: a sequential HTTP client with proper error handling and progress bar display. Its download_one function is also used by flags2_threadpool.py <recall the refactoring process for turning a sequential script into a concurrent script>

    flags2_threadpool.py: concurrent HTTP client based on futures.ThreadPoolExecutor to demonstrate error handling and integration of the progress bar

    flags2_asyncio.py: same functionality as previous example but implemented with asyncio and aiohttp. <covered in the next chapter>
***Important: be careful when testing concurrent HTTP clients on public HTTP servers so you don't get soft banned***

Learned about TQDM and its progress bar <take a look at the example below>
'''
# example - progress bar output in terminal
import time
from tqdm import tqdm

for i in tqdm(range(1000)):
    time.sleep(.01)
print('Done!')

'''
consumes any iterable and produces an iterator which, while it's consumed, displays the progress bar and estimates the remaining time to complete all iterations
    -tqdm needs to get an iterable that has a len, or receive as a second argument the expected number of items 

also implemented a command line interface -h --> will show the user help options
*take a look at example 17-8: Help screen for scripts in the flags2 series

Important arguments in flags2:
    *-s/--server: lets you choose which HTTP server and base URL will be used in the test. User can choose from the following 4:
    <Hosts with nginx>
        Local: http://localhost:8001/flags
        Remote: http://flupy.org/data/flags
        Delay: http://localhost:8002/flags; proxy delaying HTTP responses should be listened @ port 8002.
        Error: https://localhost:8003/flags; proxy introducing HTTP errors and delaying responses @ port 8003

Setting up Nginx for Localhost:
Instructions:
    https://github.com/fluentpython/example-code/blob/master/17-futures/countries/README.rst
    if you get "nginx - nginx: [emerg] bind() to [::]:80 failed (98: Address already in use)" error:
        sudo pkill -f nginx
        sudo systemctl start nginx

*************Had to change file save path in ./fluent_practice/17-futures-py3.7/countries******************

Install and running Vaurien:
Instructions:
    *installed using a virtual env as it ONLY works on Python2.7*
        virtualenv -p /usr/bin/python env  <this is the path to my python2.7>
            python <type this in terminal to check python version>
        pip install vaurien <install vaurien>
        ./vaurien_delay.sh <run the vaurien_delay.sh script in countries folder>

Testing flags.py:
$python3.7 flags_py
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
20 flags downloaded in 1.38s

Testing flags2_sequential.py:
$python3.7 flags2_sequential.py
LOCAL site: http://localhost:8001/flags
Searching for 20 flags: from BD to VN
1 concurrent connection will be used.
100%|██████████████████████████████████████████| 20/20 [00:00<00:00, 210.53it/s]
--------------------
20 flags downloaded.
Elapsed time: 0.21s

Testing flags2_threadpool.py:
$python3.7 flags2_threadpool.py
LOCAL site: http://localhost:8001/flags
Searching for 20 flags: from BD to VN
20 concurrent connections will be used.
100%|████████████████████████████████████████| 20/20 [00:00<00:00, 71575.15it/s]
--------------------
20 flags downloaded.
Elapsed time: 0.06s

Testing flags2_asyncio.py to get 100 flags (-al 100) from the Error server, using 100 concurrent requests:
$python3.7 flags2_asyncio.py -s ERROR -al 100 -m 100
Searching for 100 flags: from AD to LK
100 concurrent connections will be used.
100%|███████████████████████████████████████| 100/100 [00:00<00:00, 1120.88it/s]
--------------------
0 flags downloaded.
100 errors.
Elapsed time: 0.09s

Now that we've tested the user interface - let's look at how they were implemented


Error handling in the flags2 examples:

404 Errors (Not Found) are handled by the function in charge of downloading a single file (download_one) in all scripts
Any other exception is handled by the download_many function
'''

# take a look at flags2_sequential.py

