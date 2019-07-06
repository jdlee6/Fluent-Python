import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

# BEGIN FLAGS2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    # get_flag does NO error handling it uses the requests.Response.raise_for_status to raise an exception for any HTTP code other than 200
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    # download_one catches requests.exceptions.HTTPError to handle HTTP code 404 specifically
    except requests.exceptions.HTTPError as exc: 
        res = exc.response
        if res.status_code == 404:
            # by setting its local status to HTTPStatus.not_found; HTTPStatus is an Enum imported from flags2_common
            status = HTTPStatus.not_found  
            msg = 'not found'
        # Any other HTTPError exception is re-raised; other exceptions will just propagate to the caller
        else: 
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    # If the -v/--verbose command-line option is set, the country code and status message will be displayed; this is how you'll see progress in the verbose mode
    if verbose:  
        print(cc, msg)

    # The Result namedtuple returned by download_one, will have a status field with a value of HTTPStatus.not_found or HTTPStatus.ok
    return Result(status, cc) 
# END FLAGS2_BASIC_HTTP_FUNCTIONS


# BEGIN FLAGS2_DOWNLOAD_MANY_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
    # This Counter will tally the different download outcomes: HTTPStatus.ok, HTTPStatus.not_found, or HTTPStatus.error
    counter = collections.Counter()
    # cc_iter holds the list of the country codes received as arguments, ordered alphabetically
    cc_iter = sorted(cc_list) 
    if not verbose:
        # if not running in verbose mode, cc_iter is passed to the tqdm function which will return an iterator that yields the items in cc_iter while also displaying the animated progress bar
        cc_iter = tqdm.tqdm(cc_iter)
    # This for loop iterates over cc_iter and ...
    for cc in cc_iter: 
        try:
            # ... performs the download by successive calls to download_one
            res = download_one(cc, base_url, verbose) 
        # HTTP-related exceptions raised by get_flag and NOT handled by download_one are handled here
        except requests.exceptions.HTTPError as exc:
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        # Other network-related exceptions are handled here. Any other exception will abort the script, because the flags2_common.main function which calls download_many has no try/except
        except requests.exceptions.ConnectionError as exc:
            error_msg = 'Connection error'
        # If no exception escaped download_one then the status is retrieved from the HTTPStatus namedtuple returned by download_one
        else:
            error_msg = ''
            status = res.status

        if error_msg:
            # If there was an error, set the local status accordingly
            status = HTTPStatus.error
        # Increment the counter by using the value of the HTTPStatus Enum as key
        counter[status] += 1 
        # If running in verbose mode, display the error message for the current country code, if any
        if verbose and error_msg:
            print('*** Error for {}: {}'.format(cc, error_msg))

    # Return the counter so that the main function can display the numbers in its final report
    return counter
# END FLAGS2_DOWNLOAD_MANY_SEQUENTIAL

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)


''' 
study and review flags2_sequential.py so you can compare the differences to the concurrent files
focus on how download_many() reports progress, handles errors, and tallies downloads 
'''