# example - sentence_gen.py: Sentence implemented using a generator function

import re, reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # iterate over self.word
        for word in self.words:
            # yield the current word
            yield word
        # this return is NOT needed; the function can just "fall-through" and return automatically. 
        # Either way, a generator function doesn't raise StopIteration: it simply EXITS when it's done producing values
        return

# No need for a separate iterator class
# done


'''
__iter__ is a generator function which, when called, builds a generator object which implements the iterator interface so the SentenceIterator class is NO longer needed

not lazy as it could be
*laziness is a good trait; lazy implementation postpones producing values to the last possible moment and this SAVES meory and may avoid useless processing
'''
