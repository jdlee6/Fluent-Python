from osconfeed import load
from explore0 import FrozenJSON

raw_feed = load()
# build a FrozenJSON instance from the raw_feed made of nested dicts and lists
feed = FrozenJSON(raw_feed)

# FrozenJSON allows traversing nested dicts by using attribute notation; here we show the length of the list of speakers
print(len(feed.Schedule.speakers))
# 357

# Methods of the underlying dicts can also be accessed, like .keys(), to retrieve the record collection names
print(sorted(feed.Schedule.keys()))
# ['conferences', 'events', 'speakers', 'venues']

# Using items() we can retrieve the record collection names and their contents, to display the len() of each of them
for key, value in sorted(feed.Schedule.items()):
    print('{:3} {}'.format(len(value), key))
#   1 conferences
# 494 events
# 357 speakers
#  53 venues

# A list, such as feed.Schedule.speakers remains a list, but the items inside are converted to FrozenJSON
print(feed.Schedule.speakers[-1].name)
# Carina C. Zona

talk = feed.Schedule.events[40]
# Item 40 in the events list was a JSON object, now it's a FrozenJSON instance
print(type(talk))
# <class 'explore0.FrozenJSON'>

print(talk.name)
# There *Will* Be Bugs

# Event records have a speakers list with speaker serial numbers
print(talk.speakers)
# [3471, 5199]

# Trying to read a missing attribute raises KeyError, instead of the usual AttributeError
print(talk.flavor)
# Traceback (most recent call last):
# ...
# KeyError: 'flavor'