# BEGIN FLAGS2_THREADPOOL
import collections
from concurrent import futures

import requests
# import the progress bar display library
import tqdm  

# Import one function and one Enum from the flags2_common module
from flags2_common import main, HTTPStatus
# Reuse the download_one from flags2_sequential
from flags2_sequential import download_one 

# If the -m/--max_req command line option is NOT given, this will be the maximum number of concurrent requests, implemented as the size of the threadpool; the actual number may be smaller, if the number of flags to download is smaller
DEFAULT_CONCUR_REQ = 30
# MAX_CONCUR_REQ caps the maximum number of concurrent requests regardless of the number of flags to download or the -m/--max_req command-line option; it's a safety precaution
MAX_CONCUR_REQ = 1000 


def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    # Create the executor with max_workers set to concur_req, computed by the main function as the smaller of: MAX_CONCUR_REQ, the length of cc_list and the value of the -m/--max_req command-line portion. This avoids creating more threads than necessary
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        # this dict will map each Future instance - representing one download - with the respective country code for error reporting
        to_do_map = {} 
        # iterate over the list of country codes in alphabetical order. The order of the results will depend on the timing of the HTTP responses more than anything, but if the size of the thread pool (given by concur_req) is much smaller than len(cc_list) you may notice the downloads batched alphabetically
        for cc in sorted(cc_list): 
            # Each call to executor.submit SCHEDULES the execution of one callable and returns a Future instance. The first argument is the callable, the rest are the arguments it will receive
            future = executor.submit(download_one,
                            cc, base_url, verbose)
            # Store the future (key) and the country code in the dict
            to_do_map[future] = cc
        # futures.as_completed returns an iterator that yields futures as they are done
        done_iter = futures.as_completed(to_do_map) 
        if not verbose:
            # If not in verbose mode, wrap the result of as_completed with the tqdm function to display the progress bar; since the done_iter has NO len, we must tell tqdm what is the expected number of items as the total= argument, so tqdm can estimate the work remaining
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list)) 
        # Iterate over the futures as they are completed
        for future in done_iter:
            try:
                # Calling the result method on a future either returns the value returned by the callable, or raises whatever exceptions that were caught when the callable was executed. This method may block waiting for a resolution but NOT in this example because as_completed ONLY returns futures that are done
                res = future.result()
            # Handle the potential exceptions; the rest of this function is identical to the sequential version of download_many, except for the next call out
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                # To provide context for the error message, retrieve the country code from the to_do_map using the current future as key. This was NOT necessary in the sequential version because we were iterating over the list of country codes, so we had the current cc; here we are iterating over the futures
                cc = to_do_map[future] 
                print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# END FLAGS2_THREADPOOL

'''
this example iterates over futures with executor.submit() and futures.as_completed 
    (building a dict to map each future to other data that may be useful when the future is completed)

to_do_map maps each future to the country code assigned to it which makes it easy for processing the result of the futures
'''