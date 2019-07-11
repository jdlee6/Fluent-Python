''' debug; figure out why I keep getting errors '''

# schedule2.py (part 1): imports, constants, and the enhanced Record class

import warnings
# inspect will be used in the load_db function
import inspect

import osconfeed

# Since we are storing instances of different classes, we create and use a DIFFERENT database file, 'schedule2_db', instead of 'schedule_db' we used in schedule1.py
DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'

class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # an __eq__ method is always handy for testing    
    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


# schedule2.py (part 2): MissingDatabaseError and DbRecord class

class MissingDatabaseError(RuntimeError):
    # Custom exceptions are usually marker classes, with no body. A docstring explaining the usage of the exception is better than a mere pass statement
    ''' raised when a database is required but was not set '''

# DbRecord extends Record (inherits from Record)
class DbRecord(Record):

    # The __db class attribute will hold a reference to the openeed shelve.Shelf database
    __db = None
    
    # set_db is a staticmethod to make it explicit that its effect is ALWAYS exactly the same, no matter how it's called
    @staticmethod
    def set_db(db):
        # even if this method is invoked as Event.set_db(my_db), the __db attribute will be set in the DbRecord class
        DbRecord.__db = db
    
    # get_db is also a staticmethod because it will ALWAYS return the object referenced by DbRecord.__db, no matter how it's invoked
    @staticmethod
    def get_db(db):
        return DbRecord.__db

    # fetch is a class method so that its behavior is easier to customize in subclasses
    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            # this retrieves the record with the ident key from the database
            return db[ident]
        except TypeError:
            # if we get a TypeError and db is None, raise a custom exception explaining that the database MUST be set
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            # otherwise, re-raise the exception because we do NOT know how to handle it
            else:
                raise
        
        def __repr__(self):
            # if the record has a serial attribute, use it in the string representation
            if hasattr(self, 'serial'):
                cls_name = self.__class__.__name__
                return '<{} serial={!r}>'.format(cls_name, self.serial)
            else:
                # otherwise, default to the inherited __repr__
                return super().__repr__()

# schedule2.py (part 3): the Event class

# Event extends DbRecord (inherits from DbRecord)
class Event(DbRecord):

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_special)
        # the venue property builds a key from the venue_serial attribute and passes it to the fetch class method, inherited from DbRecord 
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        # the speakers property checks if the record has a _speaker_objs attribute
        if not hasattr(self, '_speaker_objs'):
            # if it doesn't, the 'speakers' attribute is retrieved directly from the instance __dict__ to avoid an infinite recursion, because the public name of this property is also speakers
            spkr_serials = self.__dict__['speakers']
            # get a reference to the fetch class method (the reason for this will be explained shortly)
            fetch = self.__class__.fetch
            # self._speaker_objs is loaded with a list of speaker records, using fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key) for key in spkr_serials)]
        
        # that list is returned
        return self._speaker_objs

    def __repr__(self):
        # if the record has a name attribute, use it in the string representation
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            # otherwise, default to the inherited __repr__
            return super().__repr__()

# schedule2.py (part 4): the load_db function

def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        # so far, no changes from the load_db in schedule1.py
        record_type = collection[:-1]
        # capitalize the record_type to get a potential class name; e.g 'event' becomes 'Event'
        cls_name = record_type.capitalize()
        # get an object by that name from the module global scope; get DbRecord if there's no such object
        cls = globals().get(cls_name, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            # ... bind the factory name to it. This means factory may be any subclass of DbRecord, depending on the record_type
            factory = cls
        else:
            # otherwise, bind the factory name to DbRecord
            factory = DbRecord
        # the for loop which creates the key and saves the records is the same as before, except that ... 
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            # ... the object stored in the database is constructed by factory, which may be DbRecord or a subclass selected according to the record_type
            db[key] = factory(**record)


# DbRecord.set_db(DB_NAME)
# event = DbRecord.fetch('event, 33950')
# print(event)