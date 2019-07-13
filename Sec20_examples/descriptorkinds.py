# descriptorkinds.py: simple classes for studying descriptor overriding behaviors

''' auxiliary functions for display only (not important) '''

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls is [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}._{}_({})'.format(cls_name(args[0]), name, pseudo_args))


''' essential classes for this example '''

# a typical overriding descriptor class with __get__ and __set__
class Overriding:
    '''aka data descriptor or enforced descriptor'''
    
    def __get__(self, instance, owner):
        # the print_args function is called by every descriptor method in this example
        print_args('get', self, instance, owner)
    
    def __set__(self, instance, value):
        print_args('set', self, instance, value)


# An overriding descriptor without __get__ method
class OverridingNoGet:
    '''an overriding descriptor without "__get__"'''
    
    def __set__(self, instance, value):
        print_args('set', self, instance, value)


# no __set__ method here, so this is a non-overriding descriptor
class NonOverriding:
    '''aka non-data or shadowable descriptor'''

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)
    

# the managed class, using one instance of each of the descriptor classes
class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    # the spam method is here for comparison, since methods are also descriptors
    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))