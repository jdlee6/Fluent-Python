# osconfeed.py: Downloading osconfeed.json
from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'

def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        # Issue a warning if a new download will be made
        warnings.warn(msg)
        # with using 2 context managers to read the remote file and save it
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

        # the json.load() function parses a JSON file and returns native Python objects. In this feed we have the types: dict, list, str, and int
        with open(JSON) as fp:
            return json.load(fp)


# osconfeed.py (continued): doctests for osconfeed.py

# # feed is a dict holding nested dicts and lists, with string and integer values
# feed = load()
# # List the four record collections inside "Schedule"
# print(sorted(feed['Schedule'].keys()))
# for key, value in sorted(feed['Schedule'].items()):
#     # Display record counts for each collection
#     print('{:3} {}'.format(len(value), key))

# #   1 conferences
# # 494 events
# # 357 speakers
# #  53 venues

# # navigate through the nested dicts and lists to get the name of the last speaker
# print(feed['Schedule']['speakers'][-1]['name'])
# # Carina C. Zona

# # get serial number of that same speaker
# print(feed['Schedule']['speakers'][-1]['serial'])
# # 141590

# print(feed['Schedule']['events'][40]['name'])
# # There *Will* Be Bugs

# # each event has a "speakers" list with 0 or more speaker serial numbers
# print(feed['Schedule']['events'][40]['speakers'])
# # [3471, 5199]