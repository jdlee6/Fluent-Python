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
    the classes manage an internal pool of worker threads or processes, and a queue of taks to be executed
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
'''