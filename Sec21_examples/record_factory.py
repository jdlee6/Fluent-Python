# record_factory.py: a simple class factory

def record_factory(cls_name, field_names):
    try:
        # duck typing in practice: try to split field_names by commas or spaces; if that FAILS, assume it's already an iterable, with one name per item
        field_names = field_names.replace(',',' ').split()
    # no .replace or .split
    except AttributeError:
        # assume it's already a sequence of identifiers
        pass 
    # build a tuple of attribute names, this will be the __slots__ attribute of the new class; this ALSO sets the order of fields for unpacking and __repr__
    field_names = tuple(field_names)

    # this function will become the __init__ method in the new class. It accepts positional and/or keyword arguments
    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    # implement an __iter__ so the class instances will be iterable; yield the field values in the order given by the __slots__
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)
    
    # Produce the nice repr, iterating over __slots__ and self
    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    # assemble dictionary of class attributes
    cls_attrs = dict(__slots__ = field_names,
                             __init__ = __init__,
                             __iter__ = __iter__,
                             __repr__ = __repr__)
    
    # build and return the new class, calling the type constructor
    return type(cls_name, (object,), cls_attrs)