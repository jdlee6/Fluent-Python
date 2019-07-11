# explore1.py: append a _ to attribute names that are Python keywords

import keyword

def __init__(self, mapping):
    self.__data = {}
    for key, value in mapping.items():
        # the keyword.iskeyword(...) function is exactly what we need; to use it, the keyword module must be imported
        if keyword.iskeyword(key):
            key += '_'
        self.__data[key] = value