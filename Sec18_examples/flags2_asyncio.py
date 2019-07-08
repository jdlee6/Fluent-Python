# flags2_asyncio.py: progress bar and error handling (python3.6)

import asyncio
import collections
import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

# this custom exception will be used to wrap other HTTP or network exceptions and carry the country_code for error reporting
class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code

@asyncio.coroutine
# get_flag will either return the bytes of the image downloaded, raise web.HTTPNotFound if the HTTP response status is 404 or raise an aiohttp.HttpProcessingError for other HTTP status codes
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(code=resp.status, message=resp.reason, headers=resp.headers)

@asyncio.coroutine
# The semaphor argument is an instance of asyncio.Semaphore, a synchronization device that LIMITS the number of concurrent requests
def download_one(cc, base_url, semaphor, verbose):
    try:
        # A semaphore is used as a context manager in a yield from expression so that the system as a whole is NOT blocked: only this coroutine is blocked while the semaphore counter is at the maximum allowed number
        # guarantees that NO MORE than concur_req instances of get_flags coroutines will be started at any time
        with (yield from semaphore):
            # When this with statement exits, the semaphore counter is decreased, unblocking some other coroutine instance that may be waiting for the same semaphore object
            image = yield from get_flag(base_url, cc)
    # if the flag was NOT found, just set the status for the Result accordingly
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        # Any other exception will be reported as a FetchError with the country code and the original exception chained using the raise X from Y syntax 
        # Explicit Exception Chaining
        raise FetchError(cc) from exc
    else:
        # this function call actually saves the flag image to disk
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)    
    return Result(status, cc)

'''
note: get_flag() and download_one() changed SIGNIFICANTLY compared to the sequential version because these functions are NOW coroutines using "yield from" to make asynchronous calls

note: ALWAYS should use some throttling to AVOID pounding the server with too many requests 
    *in flags2_threadpool.py: we used ThreadPoolExecutor with the required max_workers argument
    *in flags2_asyncio.py: we used asyncio.Semaphore which is created by the downloader_coro function and is passed as the semaphore argument to download_one

A Semaphore is an object that holds an internal counter that is DECREASED whenever we call the .acquire() coroutine method on it and INCREASED when we call .release() coroutine method
    *Initial value of the counter is created when the Semaphore is instantiated
        semaphore = asyncio.Semaphore(concur_req)

*.acquire() does NOT block when counter is GREATER than zero but if counter is zero, .acquire() WILL block the calling coroutine until some other coroutine calls .release() on the same Semaphore
'''

@asyncio.coroutine
# The coroutine receives the same arguments as download_many, but it CANNOT be invoked directly from main precisely because it is a coroutine function and NOT a plain function like download_many
def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    # create an asyncio.Semaphore that will allow up to concur_req active coroutines among those using this semaphore
    semaphore = asyncio.Semaphore(concur_req)
    # create a list of coroutine objects, one per call to the download_one coroutine
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]

    # get an iterator that will return futures as they are done
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        # wrap the iterator in the tqdm function to display progress
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    # iterate over the completed futures; this loop is very similar to the one in download_many in flags2_threadpool.py; most changes have to do with exception handling because of differences in the HTTP libraries (requests vs aiohttp)
    for future in to_do_iter:
        try:
            # The easiest way to retrieve the result of an asyncio.Future is using "yield from" instead of calling future.result()
            res = yield from future
        # every exception in download_one is wrapped in a FetchError with the original exception chained
        except FetchError as exc:
            # get the country code where the error occurred from the FetchError exception
            country_code = exc.country_code
            try:
                # try to retrieve the error message from the original exception (__cause__)
                error_msg = exc.__cause__.args[0]
            except IndexError:
                # if the error message CANNOT be found in the original exception, use the name of the chained exception class as the error message
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status
        # tally the outcomes
        counter[status] += 1

    # return the  counter, as done in the other scripts
    return counter

def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    # download_many simply instantiates the coroutine and passes it to the event loop with run_until_complete
    counts = loop.run_until_complete(coro)
    # when all work is done, shut down the event loop and return counts
    loop.close()

    return counts

if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

'''
futures returned by asyncio.as_completed is NOT necessarily the same futures we pass into the as_completed call

Because we could NOT use the futures as keys to retrieve the country code from a dict; we implemented FetchError that wraps a network exception and holds the country code associated it, so the country code can be reported with the error in verbose mode
    if NO error then it is available as the result of the "yield from future" expression at the top of the for loop
'''