''' 
Dictionaries and Sets
'''

# Hash tables are the engines behind Python's high performance dict
# All mapping types use the basic dict so they share that the keys
# must be hashable (only the keys)

# # tuple is hashable only if all items are hashable
# tt = (1, 2, (30, 40))
# print(hash(tt))
# # 8027212646858338501

# tl = (1, 2, [30, 40])
# print(hash(tl))
# # TypeError: unhashable type: 'list'

# tf = (1, 2, frozenset([30, 40]))
# print(hash(tf))
# # 985328935373711578

# a = dict(one=1, two=2, three=3)
# b = {'one': 1, 'two': 2, 'three': 3}
# c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
# d = dict([('two', 2), ('one', 1), ('three', 3)])
# e = dict({'three': 3, 'one': 1, 'two': 2})
# print(a == b == c == d == e)
# # True

# we can use dict comprehensions to build dictionaries

#####################################################################

# dict Comprehensions

# a dictcomp builds a dict instance by producing key:value pair from any iterable

# a list of pairs can be used direct with the dict constructor

# DIAL_CODES = [
#     (86, 'China'),
#     (91, 'India'),
#     (1, 'United States'),
#     (62, 'Indonesia'),
#     (55, 'Brazil'), 
#     (92, 'Pakinstan'),
#     (880, 'Bangladesh'),
#     (234, 'Nigeria'),
#     (7, 'Russia'),
#     (81, 'Japan'),
# ]

# # here the pairs are reversed: country is the key and code is the value
# country_code = {
#     country: code for code, country in DIAL_CODES
# }
# print(country_code)
# # {'China': 86, 'India': 91, 'United States': 1, 'Indonesia': 62, 'Brazil': 55, 'Pakinstan': 92, 'Bangladesh': 880, 'Nigeria': 234, 'Russia': 7, 'Japan': 81}

# # Reversing the pairs again, values upper-cased and items filtered
# # by code < 66
# test = {
#     code: country.upper() for country, code in country_code.items() if code < 66
#     }
# print(test)
# # {1: 'UNITED STATES', 62: 'INDONESIA', 55: 'BRAZIL', 7: 'RUSSIA'}

#####################################################################

# Common mapping methods (Look at Section3.txt)
# dict, defaultdict, OrderedDict 

# Handling missing keys with setdefault

# when updating the value found (if it is mutable), using __getitem__
# or get is awkward and inefficient

''' 
example of dict.get to fetch and update:
build an index mapping word -> list of occurences
'''
# import sys, re

# WORD_RE = re.compile(r'\w+')

# index = {}
# with open(sys.argv[1], encoding='utf-8') as fp:
#     # enumerate(iterable, start=0) 
#     for line_no, line in enumerate(fp, 1):
#         for match in WORD_RE.finditer(line):
#             word = match.group()
#             column_no = match.start()+1
#             location = (line_no, column_no)
#             # this is ugly; coded like this to make that point
#             # get the list of occurences for word, or [] if not found
#             occurences = index.get(word, [])
#             # append new location to occurences
#             occurences.append(location)
#             # put changed occurences into to index dict; this entails  second search through the index
#             index[word] = occurences

# # print in alphabetical order
# # in the key= argument of sorted I am not calling str.upper, just passing a reference to that method 
# # so the sorted function can use it to normalize the words for soring
# for word in sorted(index, key=str.upper):
#     print(word, index[word])


# # a [(19, 48), (20, 53)]
# # Although [(11, 1), (16, 1), (18, 1)]
# # ambiguity [(14, 16)]
# # and [(15, 23)]
# # are [(21, 12)]
# # aren [(10, 15)]
# # ...

'''
three lines dealing with occurences can be replaced by a single line using dict.setdefault
look at the example below
'''

# import sys, re

# WORD_RE = re.compile(r'\w+')
# index = {}

# with open(sys.argv[1], encoding='utf-8') as fp:
#     for line_no, line in enumerate(fp, 1):
#         for match in WORD_RE.finditer(line):
#             word = match.group()
#             column_no = match.start()+1
#             location = (line_no, column_no)
#             # get the list of occurences for word, or it set to [] if not found
#             # setdefault returns the value, so it can be updated without requiring a second search
#             index.setdefault(word, []).append(location)

# # print in alphabetical order
# for word in sorted(index, key=str.upper):
#     print(word, index[word])

#####################################################################

# Mapping with flexible key lookup

# defaultdict: another take on missing keys
# defaultdict is configured to create items on demand whenever a missing key is searched

'''
dd= defaultdict(list)
if 'new-key' is not in dd then the expression dd['new-key] does:
    1. calls list() to create a NEW list
    2. inserts the list into dd using 'new-key' as key
    3. retrusn a reference to that list

if dd is a defaultdict and k is a missing key, dd[k]
will call the default_factory to create a default value, but
dd.get(k) still returns None
'''

# import sys, re, collections

# WORD_RE = re.compile(r'\w+')

# # creates a defaultdict with the list constructor as default_factory
# index = collections.defaultdict(list)
# with open(sys.argv[1], encoding='utf-8') as fp:
#     for line_no, line in enumerate(fp, 1):
#         for match in WORD_RE.finditer(line):
#             word = match.group()
#             column_no = match.start()+1
#             location = (line_no, column_no)
#             # if word is not initially in the index, the default_factory is called
#             # to produce the missing value, which in this case is an empty list that is then 
#             # assigned to index[word] and returned, so the .append(location) operation
#             # always succeeds
#             index[word].append(location)

# # print in alphabetical order
# for word in sorted(index, key=str.upper):
#     print(word, index[word])


# The __missing__ method

''' 
if you subclass dict and provide a __missing__ method,
the standard dict.__getitem__ will call it whenever a key
is not found, instead of raising KeyError
'''

'''
When searching for a non-string key, StrKeyDict0 converts 
it to str when it is NOT found
'''

# # StrKeyDict0 inherits from dict
# class StrKeyDict0(dict):
#     def __missing__(self, key):
#         # Check whether key is already a str
#         # If it is, and it's missing, raise KeyError
#         if isinstance(key, str):
#             raise KeyError(key)
#         # Build str from key and look it up
#         return self[str(key)]

#     def get(self, key, default=None):
#         try:
#             # The get method delegates to __getitem__ by using the self[key] notation
#             # that gives the opportunity for our __missing__ to act
#             return self[key]
#         # if a KeyError was raised, __missing__ already failed, so we return the default
#         except KeyError:
#             return default

#     def __contains__(self, key):
#         # Search for unmodified key (the instance may contain non-str keys), then for a str built from the key
#         return key in self.keys() or str(key) in self.keys()

# # Tests for item retrieval using 'd[key]' notation
# d = StrKeyDict0([('2', 'two'), ('4', 'four')])
# print(d['2'])
# # two
# print(d[4])
# # four
# print(d[1])   
# # raise KeyError(key)
# # KeyError: '1'

# # Tests for item retrieval using 'd.get(key)' notation
# print(d.get('2'))
# # two
# print(d.get(4))
# # four
# print(d.get(1, 'N/A'))
# # N/A

# # Tests for the 'in' operator
# print(2 in d)
# # True
# print(1 in d)
# # False

#####################################################################

# Variations of dict

'''
collections.OrderedDict - maintains keys in insertion order (iteration over items in predictable order)

collections.Chainmap - holds list of mappings which can be searched as one 
(maps attribute to create new subcontexts and a property for accessing all but the first mapping)

collections.Counter - a mapping that holds an integer count for each key

collections.UserDict - pure Python implementation of mapping that works like a standard dict 
(designed to be subclassed)
'''
# import collections
# ct = collections.Counter('abracadabra')
# print(ct)
# # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# ct.update('aaaaaazzz')
# print(ct)
# # Counter({'a': 11, 'z': 3, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# print(ct.most_common(2))
# # [('a', 11), ('z', 3)]


# Subclassing UserDict.
# almost always easier to create a new mapping type by extending UserDict than dict.
# UserDict does not inherit from dict but has an internal dict instance called data which 
# holds the actual items

# import collections
# # StrKeyDict extends UserDict
# class StrKeyDict(collections.UserDict):

#     # __missing__ is exactly as the example above
#     def __missing__(self, key):
#         if isinstance(key, str):
#             raise KeyError(key)
#         return self[str(key)]

#     # __contains__ is simpler: we can assume all stored
#     # keys are str and we can check on self.data instead of
#     # invoking self.keys() as we did in StrKeyDict0
#     def __contains__(self, key):
#         return str(key) in self.data

#     # __setitem__ converts any key to a str. This method is easier 
#     # to overwrite when we can delegate to the self.data attribute
#     def __setitem__(self, key, item):
#         self.data[str(key)] = item

''' 
UserDict subclasses MutableMapping, the remaing methods
that make StrKeyDict a full-fledged mapping are inherited from
UserDict, MutableMapping, Mapping

MutableMapping.update 
Mapping.get
'''

#####################################################################

# Immutable mappings

# example is the Pingo.io project and the board.pins mapping which represent the
# physical GPIO pins on the device - hardware can't be changed via software
# so any change in mapping would make it inconsistent

# MappingProxyType wrapper class from types module 
# returns a mappingproxy instance that is a read-only but dynamic view of original 
# mapping (changes cannot be made through it)

# from types import MappingProxyType

# d={1: 'A'}
# d_proxy = MappingProxyType(d)
# print(d_proxy)
# # {1: 'A'}

# # items in d can be seen through d_proxy
# print(d_proxy[1])
# # A

# # changes cannot be made through d_proxy
# # print(d_proxy[2])
# # KeyError: 2

# d[2] = 'B'
# # d_proxy is dynamic: any change in d is reflected 
# print(d_proxy)
# # {1: 'A', 2: 'B'}

# print(d_proxy[2])
# # B

#####################################################################

# Set Theory

# A set is a collection of unique objects (basic use case is to remove duplicates)
# elements must be hashable while the set type is NOT hashable although
# frozenset is HASHABLE so you can have frozenset elements inside a set
# l = ['spam', 'spam', 'eggs', 'spam']
# print(set(l))
# # {'eggs', 'spam'}
# print(list(set(l)))
# # ['eggs', 'spam']

'''
a | b - returns their union
a & b - computes their intersection
a - b - computes their difference 
'''

# Count occurences needles in a haystack, both of type set 
# found = len(needles & haystacks)

# without sets, we would have to code something like below
# this runs for ANY iterables unlike the example above
# found = 0 
# for n in needles:
#     if n in haystack:
#         found += 1

# if no sets then create them
# found = len(set(needles) & set(haystack)) 

# another way is below:
# found = len(set(needles).intersection(haystack))

# set literals
