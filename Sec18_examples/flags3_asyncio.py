# flags3_asyncio.py - More coroutine delegation to perform 2 requests per flag

'''
download_many and download_coro are UNCHANGED from flags2_asyncio.py

changes:
    download_one
        coroutine now uses "yield from" to delegate to "get_flag" and the new "get_country" coroutine
    
    get_flag
        most code from this coroutine was moved to a new http_get coroutine so it can also be used by "get_country"

    get_country
        this coroutine fetches the metadata.json file for the country code and gets the name of the country from it

    http_get
        common code for getting a file from the web
'''
import asyncio
import collections
import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag


DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


@asyncio.coroutine
def http_get(url):
    res = yield from aiohttp.request('GET', url)
    if res.status == 200:
        ctype = res.headers.get('Content-type', ' ').lower()
        if 'json' in ctype or url.endswith('json'):
            # if the content type has 'json' in it or the url ends with .json, use the response .json() method to parse it and return a Python data structure - in this case, a dict
            data = yield from res.json()
        else:
            # otherwise use .read() to fetch the bytes as they are
            data = yield from res.read()
        return data

    elif res.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.errors.HttpProcessingError(code=res.status, message=res.reason, headers=res.headers)


@asyncio.coroutine
def get_country(base_url, cc):
    url = '{}/{cc}/metadata.json'.format(base_url, cc=cc.lower())
    # metadata will receive a Python dict built from the JSON contents
    metadata = yield from http_get(url)
    return metadata['country']


@asyncio.coroutine
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    # The outer parenthesis here are required because the Python parser gets confused and produces a syntax error when it sees the keywords return yield from lined up like that
    return (yield from http_get(url))


@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):
    try:
        # I put the calls to get_flag and get_country in separate with blocks controlled by the semaphore because I want to keep it acquired for the shortest possible time
        with (yield from semaphore):
            image = yield from get_flag(base_url, cc)
        with (yield from semaphore):
            country = yield from get_country(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        country = country.replace(' ', '_')
        filename = '{}-{}.gif'.format(country, cc)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_flag, image, filename)
        status = HTTPStatus.ok
        msg = 'OK'
    
    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]

    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        try:
            res = yield from future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status
        counter[status] += 1

    return counter


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()

    return counts

if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

'''
usage of "yield from"
you "yield from" coroutines and asyncio.Future instances - including tasks

play with the scripts with the command line options:
    -a 
    -e
    -l
        these control the number of downloads
    -m
        to set the number of concurrent downloads
    LOCAL
    REMOTE
    DELAY
    ERROR
'''