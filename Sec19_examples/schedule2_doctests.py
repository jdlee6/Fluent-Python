# schedule2_doctests.py: extract from the doctests of schedule2.py

from schedule2 import *
import shelve

# open the database with shelve and reference it by assigning it to the db variable
db = shelve.open(DB_NAME)
if CONFERENCE not in db:
    load_db(db)

# DbRecord extends Record, adding database support: to operate, DbRecord MUST be given a reference to a database
DbRecord.set_db(db)

# The DbRecord.fetch class method retrieves records of any type
event = DbRecord.fetch('event.33950')

# Note that event is an instance of the Event class, which extends DbRecord
print(event)
# <Event 'There *Will* Be Bugs'>

# Accessing the event venue returns a DbRecord instance
print(event.venue)
# <DbRecord serial='venue.1449'>

# Now it's easy to find out the name of an event.venue. This automatic dereferencing is the GOAL of this example
print(event.venue.name)
# Portland 251

# we can also iterate over the event.speakers list, retrieving DbRecords representing each speaker
for spkr in event.speakers:
    print(f'{spkr.serial}, {spkr.name}')

# speaker.3471, Anna Ravenscroft
# speaker.5199, Alex Martelli