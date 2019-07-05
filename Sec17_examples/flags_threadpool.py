# script 2 - flags_threadpool.py: threaded download script using futures.ThreadPoolExecutor
from concurrent import futures

# reuse some functions from the flags module
from flags import save_flag, get_flag, show, main

# maximum number of threads to be used in the ThreadPoolExecutor
MAX_WORKERS = 20

# Function to download a single image; this is what each thread will execute
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')

def download_many(cc_list):
    # set the number of worker threads: use the smaller number between the maximum we want to allow (MAX_WORKERS and the actual items to be processed, so no unnecessary threads are created
    workers = min(MAX_WORKERS, len(cc_list))
    # Instantiate the ThreadPoolExecutor with that number of worker threads; the executor.__exit__ method will call executor.shutdown(wait=True), which will block until all threads are done
    with futures.ThreadPoolExecutor(workers) as executor:
        # The map method is similar to the map built-in, except that the download_one function will be called concurrently from multiple threads; it returns a generator that can be iterated over to retrieve the value returned by each function
        res = executor.map(download_one, sorted(cc_list))
    
    # Return the number of results obtained; if any of the threaded calls raised an exception, that exception would be raised here as the implicit next() call tried to retrieve the corresponding return value from the iterator
    return len(list(res))

if __name__ == "__main__":
    # call the main function from the flags module, passing the enhanced version of download_many
    main(download_many)

'''
download_one() is essentially the body of the for loop in flags.py
    common refactoring when writing concurrent code: turning the body of a sequential for loop into a function to be called concurrently
'''