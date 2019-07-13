# bulkfood_v4prop.py: same functionality as bulkfood_v4.py with a property factory instead of a descriptor class

# NO storage_name argument
def quantity():
    try:
        # we can NOT rely on class attributes to share the counter across invocations, so we define it as an attribute of the quantity function itself
        quantity.counter += 1
    except AttributeError:
        # if quantity.counter is undefined, set it to 0
        quantity.counter = 0

    # we also do NOT have instance attributes, so we create storage_name as a local variable and rely on closures to keep them alive for later use by qty_getter and qty_setter
    storage_name = '_{}:{}'.format('quantity', quantity.counter)

    # the rest of the code is the same as bulkfood_v2prop.py EXCEPT that here we can use getattr and setattr built-ins INSTEAD of instance.__dict__
    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)