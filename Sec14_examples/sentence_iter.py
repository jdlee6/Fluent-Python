# example - sentence_iter.py: Sentence implemented using the Iterator pattern
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    
    # the __iter__ method is the only addition to the previous Sentence implementation. This version has NO __getitem__,  the class is iterable because it implements __iter__
    def __iter__(self):
        # __iter__ fulfills the iterable protocol by instantiating and returning an iterator
        return SentenceIterator(self.words)

class SentenceIterator:
    def __init__(self, words):
        # holds reference to the list of words
        self.words = words
        # self.index used to determine the next word to fetch
        self.index = 0

    def __next__(self):
        try:
            # Get the word at self.index
            word = self.words[self.index]
        except IndexError:
            # If there is no word at self.index, raise StopIteration
            raise StopIteration()
        # Increment self.index
        self.index += 1
        # return the word
        return word

    # implement self.__iter__
    # not needed but good practice: iterators are supposed to implement both __next__ and __iter__ (makes our iterator pass the issubclass(SentenceIterator, abc.Iterator) test)
    def __iter__(self):
        return self