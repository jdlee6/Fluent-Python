# schedule1_doctests: testing the functionality provided by schedule1.py

import shelve
from schedule1 import DB_NAME, CONFERENCE, load_db

import pprint, time

# shelve.open opens an existing or just-created database file
db = shelve.open(DB_NAME)
# a quick way to determine if the database if populated is to look for a known key in this case 'conference.115' - the key to the single conference record
if CONFERENCE not in db:
    # if the database is empty, call load_db(db) to load it
    load_db(db)

# pprint.pprint(db)
# time.sleep(1)

# this method does NOT retrieve the speaker; instead it throws a KeyError 
# this is b/c we set it up wrong in schedule1.py ('{}, {}' instead of '{}.{}')
# speaker = db['speaker.3471']

# Fetch a speaker record
speaker = db['speaker.3471']
# It's an instance of the Record class defined in schedule1.py
print(type(speaker))
# <class 'schedule1.Record'>

# Each Record instance implements a custom set of attributes reflecting the fields of the underlying JSON record
print(speaker.name, speaker.twitter)
# Anna Ravenscroft annaraven

# ALWAYS remember to close a shelve.Shelf. If possible, use a with block to make sure that the Shelf is closed.
db.close()