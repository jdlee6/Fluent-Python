# schedule1.py: exploring OSCON schedule data saved to shelve.Shelf
# focus on the idea of __init__ updating the instance __dict__

import shelve
import warnings
# load the osconfeed.py module
import osconfeed

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'

class Record:
    def __init__(self, **kwargs):
        # this is a common shortcut to BUILD an instance with attributes created from keyword arguments
        self.__dict__.update(kwargs)

def load_db(db):
    # this may fetch the JSON feed from the Web, if there's no local copy
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    # iterate over the collections (ie. 'conferences', 'events' etc.)
    for collection, rec_list in raw_data['Schedule'].items():
        # record_type is set to the collection name without the trailing 's', i.e. 'events' becomes 'event'
        record_type = collection[:-1]
        for record in rec_list:
            # build key from the record_type and the 'serial' field
            key = '{}, {}'.format(record_type, record['serial'])
            # update 'serial' field with the full key
            record['serial'] = key
            # build Record instance and save it to the database under the key
            db[key] = Record(**record)


print(Record.__dict__)

