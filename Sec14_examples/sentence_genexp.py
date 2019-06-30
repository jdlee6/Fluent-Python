# example - Sentence implemented using a generator expression

import re, reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # __iter__ method is NOT a generator function (has no yield) but uses a generator expression to build a generator and then returns it
        # end result is the same; the caller of __iter__ gets a generator object
        return (match.group() for match in RE_WORD.finditer(self.text))