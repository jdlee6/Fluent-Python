# script 3 - flags_threadpool_ac.py: replacing executor.map with executor.submit and futures.as_completed in the download_many function

from concurrent import futures

# reuse some functions from the flags module
from flags import save_flag, get_flag, show, main

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')

def download_many(cc_list):
    # for this example, use only the top 5 most populous contries
    cc_list = cc_list[:5]
    # Hard code max_workers to 3 so we can observe pending futures in the output
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        # iterate over country codes alphabetically, to make it clear that results arrive out of order
        for cc in sorted(cc_list):
            # executor.submit schedules the callable to be executed, and returns a future representing this pending operation
            future = executor.submit(download_one, cc)
            # store each future so we can later retrieve them with as_completed
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            # Display a message with the country code and the respective future
            print(msg.format(cc, future))
        
        results = []
        # as_completed yields futures as they are completed
        for future in futures.as_completed(to_do):
            # get the result of this future
            res = future.result()
            msg = '{} result: {!r}'
            # display the future and its result
            print(msg.format(future, res))
            results.append(res)

    return len(results)

if __name__ == "__main__":
    main(download_many)

'''
!Need to debug: returning None?!
'''

# The futures are scheduled in alphatebetical order; the repr() of a future shows its state: the first 3 are running because there are 3 worker threads
# Scheduled for BR: <Future at 0x100791518 state=running> 

# Scheduled for CN: <Future at 0x100791710 state=running>

# Scheduled for ID: <Future at 0x100791a90 state=running>

# The last two futures are pending, waiting for worker threads
# Scheduled for IN: <Future at 0x101807080 state=pending>

# Scheduled for US: <Future at 0x101807128 state=pending>

# The first CN here is the output of download_one in a worker thread; the rest of the line is the output of download_many
# CN <Future at 0x100791710 state=finished returned str> result: 'CN'

# Here two threads output codes before download_many in the main thread can display the result of the first thread
# BR ID <Future at 0x100791518 state=finished returned str> result: 'BR'
# <Future at 0x100791a90 state=finished returned str> result: 'ID'

# IN <Future at 0x101807080 state=finished returned str> result: 'IN'

# US <Future at 0x101807128 state=finished returned str> result: 'US'

# 5 flags downloaded in 0.70s