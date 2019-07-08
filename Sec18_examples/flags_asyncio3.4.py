# flags_asyncio3.4.py: Asynchronous download script with asyncio and aiohttp utilizing @asyncio.coroutine & yield from

'''
async def = NEW syntax for Python3.5+
"await", "async with" and "async" for keyword statements inside async def

@asyncio.coroutine is analagous to async def
"yield from" instead of "await"

take a look at flags_asyncio.py
'''

# BEGIN FLAGS_ASYNCIO
import asyncio

# aiohttp must be installed - it's NOT in the standard library
import aiohttp

# Reuse some functions from the flags modules
from flags import BASE_URL, save_flag, show, main

# Coroutines should be decorated with @asyncio.coroutine
@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    # Blocking operations are implemented as coroutines, and your code delegates to them via "yield from" so they run asynchronously
    resp = yield from aiohttp.request('GET', url) 
    # Reading the response contents is a separate asynchronous operation
    image = yield from resp.read()
    return image


@asyncio.coroutine
# download_one MUST also be a coroutine since it uses "yield from"
def download_one(cc):
    # The only difference from the sequential implementation of download_one are the words "yield from" in this line; the rest of the function is exactly as before
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # get a reference to the underlying event-loop implementation
    loop = asyncio.get_event_loop() 
    # Build a list of generator objects by calling the download_one function once for each flag to be retrieved
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    # Despite its name, wait is NOT a blocking function. It's a coroutine that completes when all the coroutines passed to it are done (default behavior of wait)
    wait_coro = asyncio.wait(to_do)  
    # Execute the event loop until wait_coro is done; this is where the script will block while the event loop runs. We ignore the second item returns by run_until_complete
    res, _ = loop.run_until_complete(wait_coro)  
    # Shut down the event loop
    loop.close() 

    return len(res)


if __name__ == '__main__':
    main(download_many)
# END FLAGS_ASYNCIO

'''
asyncio.wait() coroutine accepts an iterable of futures/coroutines; wait wraps each coroutine in a Task.
    End result: all objects managed by wait BECOME instances of Future and because it is a coroutine function, calling wait() returns a coroutine/generator object (which is what the wait_coro variable holds)
    *two arguments: timeout and return_when (arguments that may cause it to return even if INCOMPLETE)

loop.run_until_complete() function accepts a future or a coroutine (drives the coroutine)
    if coroutine: run_until_complete wraps it into a Task, similar to what wait does. 
        *coroutines, futures, tasks can all be driven by yield from and this is what run_until_complete does with the wait_coro object returned by the wait call
    when completed it returns a 2 tuple where the FIRST item is the set of completed futures and the SECOND is the set of not completed futures (we ignore the second set with the '_' character)
'''