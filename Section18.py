'''
Concurrency with asyncio

asyncio: a package that implements concurrency with coroutines driven an event loop
    uses "yield from" which makes it incompatible with older versions of Python


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
    -only one coroutine is running at any time (a coroutine can ONLY be cancleed when it's suspended at a yield point)


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
       -you DON'T need my_future.add_done_callback() because you can simply put whateer processing you would do after the future is done in the line that follow yield from my_future in your coroutine. That's the big advantage of having coroutines: functions that can be suspended and resumed
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

overview of flags_asyncio.py:
    1. we start the process in download_many by feeding the event loop with several coroutine objects produced by calling download_one
    2. the asyncio event loop activates each coroutine in turn 
    3. when a client coroutine such as get_flag uses "yield from" to delegate to a library coroutine - such as aiohttp.request - control goes BACK to the event loop, which can execute ANOTHER previously scheduled coroutine
    4. The event loop uses low-level APIs based on callbacks to get notified when a blocking operation is completed
    5. When that happens, the main loop sends a result to the suspended coroutine
    6. The coroutine then advances to the next yield, (ie "yield from resp.read()" in get_flag). The event loop takes charge again. Steps 4, 5, 6 repeat until the event loop is terminated

*similar to taxi_sim.py where the main loop started several taxi processes in turn.

*Summary: a single threaded program where a main loop activates queued coroutines one by one. Each coroutine advances a few steps, then yields control BACK to the main loop, which then activates the next coroutine in the queue.

take a look at flags_asyncio.py
'''

