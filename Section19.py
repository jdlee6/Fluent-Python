'''
Dynamic attributes and properties

data attributes and methods are collectively known as attributes
    a method is just an attribute that is callable

properties: can be used to replace a public data attribute with accessor methods (getter/setter) WITHOUT changing the class interface

__getattr__ & __setattr__
    evaluates attribute access using dot notation
        ie. obj.attr


Data wrangling with dynamic attributes
take a look at osconfeed.json
    shows 4 out of the 895 records in the JSON feed
    "serial" is the unique identifier within the list
'''

# take a look at osconfeed.py

'''
Exploring JSON-like data with dynamic attributes

the syntax feed: ['Schedule']['events'][40]['name'] is lengthy and annoying to read

in js; we can simply find our query with: "feed.Schedule.events[40].name"
    we can also implement a dict-like class that does the same in Python
'''

# take a look at class FrozenJSON in explore0.py
# take a look at explore_doctest.py

'''
**Any script that generates or emulates dynamic attribute names from arbitrary source MUST deal with one issue: the keys in the original data may NOT be suitable attribute names


The invalid attribute name problem 
...
'''

