'''
Concurrency with asyncio

asyncio: a package that implements concurrency with coroutines driven an event loop
    uses "yield from" which makes it incompatible with older versions of Python

** event loop: programming construct that waits for and dispatches events or messages in a program
        -constant collecting events and loops over them to find what to do with the event


Thread vs. Coroutine: a comparison
    *spinner_thread.py and spinner_asyncio.py

differences between the supervisor() function in both examples:
    -An asyncio.Task is roughly equivalent of a threading.Thread
    -A Task drives a coroutine; a Thread invokes a callable
    -DON'T instatiate Task objects, you get them by passing a coroutine to asyncio.async() or loop.create_task()
    -When you get a Task object, it is already scheduled to run; a Thread instance must be explicitly told to run by calling its start method
    -In the threaded supervisor, the slow_function is a plain function and is directly invoked by the thread. In the asyncio supervisor, slow_function is a coroutine driven by "yield from"
    -can NOT terminate a thread from the outside; for tasks, there is Task.cancel() instance method which raises CancelledError inside the coroutine
    -the supervisor coroutine must be executed with loop.run_until_complete in the main function

*With coroutines, everything is protected against interruption by default
    -only one coroutine is running at any time (a coroutine can ONLY be cancelled when it's suspended at a yield point)


asyncio.Future: non-blocking by design

note: futures are created only as the result of scheduling something for execution

In asyncio, BaseEventLoop.create_task() takes a coroutine, schedules it to run and returns asyncio.Task instance which is also an instance of asyncio.Future because Task is a subclass of Future designed to wrap a coroutine
    *analagous to how we create concurrent.futures.Future instances by invoking executor.submit()

    Methods of asyncio.Future:
        .done() 
        .add_done_callback()
            instead of triggering a callback, when the delayed operation is done the event loop sets the result of the future and the "yield from" expression produces a return value inside our suspended coroutine, allowing it to resume
        .result()
            in asyncio.Future, the .result() method takes NO arguments, you can't specify a timeout. 
                *if you call .result() and the future is NOT done, it does NOT block waiting for the result. Instead an asyncio.invalidStateError is raised 
                *using "yield from" with a future automatically takes care of waiting for it to finish WITHOUT blocking the event loop ("yield from" is used to give control back to the event loop)
    
    asyncio.Future summary:
       -you DON'T need my_future.add_done_callback() because you can simply put whatever processing you would do after the future is done in the line that follow yield from my_future in your coroutine. That's the big advantage of having coroutines: functions that can be suspended and resumed
       -you DON'T need my_future.result() because the value of "yield from" expression on a future is the result, ie: result = yield from my_future
    **in normal usage, asyncio futures are driven by yield from and NOT by calling those methods above


Yielding from futures, tasks, and coroutines
*close relationship between futures and coroutines because you can get the result from a "yield from" expression

In order to execute, a coroutine MUST be scheduled and then it's wrapped in an asyncio.Task; 2 ways of obtaining a Task:
    1. asyncio.async(coro_or_future, *, loop=None) <does NOT work in python3.7>
            This function unifies coroutines and futures: the first argument can be either one. If it's a Future or Task, it's returned unchanged. If it's a coroutine, async calls loop.create_task() on it to create a Task. An optional event loop may be passed as the loop= keyword agument; if ommitted, async gets the loop object by calling asyncio.get_event_loop()

    2. BaseEventLoop.create_task(coro) <from Python3.4+>
            This method schedules the coroutine for execution and returns an asyncio.Task object. If called on a custom subclass of BaseEventLoop, the object returned may be an instance of some other Task-compatible class provided by an external library


Downloading with asyncio and aiohttp
asyncio ONLY supports TCP&UDP directly
aiohttp is for asyncio HTTP clients and servers

overview of flags_asyncio3.4.py:
    1. we start the process in download_many by feeding the event loop with several coroutine objects produced by calling download_one
    2. the asyncio event loop activates each coroutine in turn 
    3. when a client coroutine such as get_flag uses "yield from" to delegate to a library coroutine - such as aiohttp.request - control goes BACK to the event loop, which can execute ANOTHER previously scheduled coroutine
    4. The event loop uses low-level APIs based on callbacks to get notified when a blocking operation is completed
    5. When that happens, the main loop sends a result to the suspended coroutine
    6. The coroutine then advances to the next yield, (ie "yield from resp.read()" in get_flag). The event loop takes charge again. Steps 4, 5, 6 repeat until the event loop is terminated

*similar to taxi_sim.py where the main loop started several taxi processes in turn.

*Summary: a single threaded program where a main loop activates queued coroutines one by one. Each coroutine advances a few steps, then yields control BACK to the main loop, which then activates the next coroutine in the queue.

take a look at flags_asyncio3.4.py
read the bottom of flags_asyncio3.4.py

*To leverage asyncio, we MUST replace every function that hits the network with an asynchronous version that is invoked with yield from, so that the control is given back to the EVENT loop
*For each request, a download_one coroutine object is created in download_many which are all driven by the loop.run_until_complete() function after being wrapped with asyncio.wait coroutine

*yield from foo syntax AVOIDS blocking because the current coroutine is SUSPENDED; when the foo future/coroutine is DONE, it retuns a result to the SUSPENDED coroutine which resumes it

2 facts about every usage of "yield from"
    1. every arrangement of coroutines chained with "yield from" must be ultimately driven by a caller that is NOT a coroutine, which invokes next() or .send() on the outermost delegating generator, explicitly or implicitly
    2. The innermost subgenerator in the chain MUST be a simple generator that uses just "yield" or an iterable object
    In addition to these facts, asyncio "yield from" also follows:
        1. coroutine chains we write are ALWAYS driven by passing our outermost delegating generator to an asyncio call, such as loop.run_until_complete()
            next()/.send() doesn't drive the coroutine chain in asyncio BUT the asyncio event loop DOES that
            *the coroutine chains we write ALWAYS end by delegating with "yield from" to some asyncio coroutine function/method (innermost subgenerator will be a library function that does the ACTUAL I/O and NOT something we write)


Running circles around blocking calls

Two ways to prevent blocking calls to halt the progress of the entire app:
    1. run each blocking operation in a separate thread
    2. turn every blocking operation into a non-blocking asynchronous call

callbacks are the traditional way to implement asynchronous calls with LOW memory overhead
    -instead of waiting for a response; we register a function to be called when something happens (this is a way to make everything NON BLOCKING)

flags.py spends billions of CPU cycles waiting for each download, one after the other (sequentially)
vs.
flags_asyncio3.4.py: when loop_until_completes is called in the download_many function, the event loop drives each download_one coroutine to the first "yield from" and this in turn drives each get_flag coroutine to the first "yield from" calling aiohttp.request()
    *NONE of these calls are blocking
    *as it gets the first response back, the event loop sends it to the waiting get_flag coroutine and as get_flag gets a reponse, it advances to the next "yield from", which calls resp.read() and yields control back to the main loop
        -as each get_flag returns, the delegating generator download_one resumes and saves the image file
**results were 70 more times faster THAN a sequential script


Enhancing the asyncio downloader script (progress bar and proper error handling)
*Recall that all flags2 set of examples share the same command line interface:

Output of flags2_asyncio.py:
$ python3 flags2_asyncio.py -s ERROR -al 100 -m 100
ERROR site: http://localhost:8003/flags
Searching for 100 flags: from AD to LK
100 concurrent connections will be used.
--------------------
73 flags downloaded.
27 errors.
Elapsed time: 0.64s

Using asyncio.as_completed (equivalent asyncio version of flags2_threadpool.py)
to update a progress bar we need to get results AS they are done (must use the asyncio equivalent of as_completed)

Take a look at flags2_asyncio.py
    study/review carefully and take a look at the notes at the bottom


Using an executor to avoid blocking the event loop
**Local filesystem access is BLOCKING in Python**

in flags2_asyncio.py:
    the BLOCKING function is save_flag
        blocks the single thread our code shares with the asyncio event loop and freezes the WHOLE application while the file is being saved
    
    SOLUTION: run_in_executor() 
        behind the scenes, asyncio event loop has a thread pool executor and you can send callables to be executed by it with run_in_executor()

take a look at flags2_asyncio_executor.py


From callbacks to futures and coroutines
"callback hell": the nesting of callbacks when one operation depends on the result of the previous operation

*take a look at callback hell on page 589 (javascript example)
*take a look at callback hell (chained callbacks) on page 590 (python example)

both examples are hard to read and harder to write:
    each function does part of the job, set up the next callback and returns, to let the event loop procceed

within a coroutine, to perform three asynchronous actions in succession, you "yield" three times to let the event loop continue running
    when the result is ready, the coroutine is activated with a .send() call (similar to invoking a callback)

take a look at the example below
'''
# # example: coroutines and yield from ENABLE asynchronous programming without callbacks
# import asyncio

# @asyncio.coroutine
# def three_stages(request1):
#     response1 = yield from api_call1(request1)
#     # stage 1
#     request2 = step1(response1)
#     response2 = yield from api_call2(request2)
#     # stage 2
#     request3 = step2(response2)
#     response3 = yield from api_call3(request3)
#     # stage 3
#     step3(response3)
#     # must explicitly schedule execution
#     loop.create_task(three_stages(request1))

'''
the example above is much easier to follow than the previous examples of callback hell
    the three stages of the operation appear ALL inside the same function (easy to follow the follow up processing)

error handling in callback hell examples are nearly impossible to deal with and make the program much more complex than needed

but using coroutines, we can just handle the potential errors by putting the "yield from" lines inside try/except blocks

sacrifices made when using coroutines:
    1. MUST use coroutines and get used to "yield from"
    2. can NOT simply call it; you must explicitly SCHEDULE the execution of the coroutine with the event loop or activate it using "yield from" in ANOTHER coroutine that is scheduled for execution
    *loop.create_task(three_stages(request1)) - this line is needed or NOTHING would happen in the example above


Doing multiple requests for each download
objective: save each country flag with the name of the country and the country code
    1. one HTTP request to get the flag image
    2. another HTTP request to get the metadata.json file (where the name of the country is recorded)

threaded script: make one request then the other, blocking the thread twice and keeping both pieces of data in local variables, ready to use when saving the files

in an asynchronous script with callbacks: need to be passed around in a closure or held somewhere until you can save the file because each callback runs in a DIFFERENT local context

coroutines: solution to asynchronous script with callbacks; not AS simple as threaded scripts but a lot more SIMPLE than asynchronous script with callbacks

take a look at flags3_asyncio.py
last example; this wraps up the flags2 set of examples

*now we will go from client scripts to learning how to write servers with asyncio*


Writing asyncio servers
*take a look at figure 18-2 on page 595


An asyncio TCP server
https://github.com/fluentpython/example-code/blob/master/18-asyncio/charfinder/charfinder.py

charfinder.py was designed to provide content for our asyncio servers
    -indexes each word that appears in character names in the Unicode database bundled with Python and creates an inverted index stored in a dict
    -if multiple words; charfinder computes the intersection of the sets retrieved from the index

take a look at tcp_charfinder.py (part 1)
    read notes at the bottom

take a look at def main() on tcp_charfinder.py (part 2)
    read notes

https://docs.python.org/3/library/asyncio-stream.html
take a look at the output on tcp_charfinder.py (part 3)
    read notes


An aiohttp Web Server
aiohttp library also supports server-side HTTP

take a look figure 18-3 on page 600
    browser window displaying search results for "cat face" on the http_charfinder.py server

*fonts on browsers may cause an issue in specific chrome and opera; if so then use firefox

take a look at http_charfinder.py (part 1: main and init functions)
    this is the bottom half where the event loop and the HTTP server is setup and torn down

take a look at http_charfinder.py (part 2: home function)
    home() is NOT a coroutine but a plain function which is part of a larger issue: need to rethink how we code web apps to achieve high concurrency


Smarter clients for better concurrency
the home() is similar to a view function in flask (nothing asynchronous; it gets a request, fetches data from database and builds a response by rendering an html page)
    *retrieving data from a database should be done asynchronously so you do NOT block the event loop

highly concurrent systems must split large chunks of work into smaller pieces to stay responsive

way to AVOID long response problems is to implement pagination and have the user click or the page to fetch more
'''
