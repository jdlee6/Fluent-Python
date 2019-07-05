# script 1 - flags.py: sequential download script. Some functions will be reused by the other scripts
import os, time, sys

# import the requests library; it's NOT part of the standard library so by convention we import it after the standard library os, time, and sys modules and separate it from them with a blank line
import requests

# List of the ISO 3166 country codes for the 20 most populous countries in order of decreasing population
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
                        'MX PH VN ET EG DE IR TR CD FR').split()

# The web site with the flag images
BASE_URL = 'http://flupy.org/data/flags'

# Local directory where the images are saved
DEST_DIR = '/home/joe/Downloads/'

# Simply save the img(a byte sequence) to filename in the DEST_DIR
def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

#  Given a country code, build the URL and download the image, returning the binary contents of the response
def get_flag(cc):
    url = f'{BASE_URL}/{cc.lower()}/{cc.lower()}.gif'
    resp = requests.get(url)
    return resp.content

# Display a string and flush sys.stdout so we can see progress in a one-line display; this is needed because Python normally waits for a line break to flush the stdout buffer
# prints it out on one line (because of the end=' '), one by one (take a look at flush.py for an example)
def show(text):
    print(text, end=' ')
    sys.stdout.flush()

# download_many is the key function to compare with the concurrent implementations you will see from the next example
def download_many(cc_list):
    # loop over the list of country codes in alphabetical order, to make it clear that the ordering is preserved in the output; return the number of country codes downloaded
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)

# main records and reports the elapsed time after running download_many;
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

if __name__ == "__main__":
    # main must be called with the function that will make the downloads; we pass the download_many function as an argument so that main can be used as a library function with other implementations of download-many in the next examples
    main(download_many)