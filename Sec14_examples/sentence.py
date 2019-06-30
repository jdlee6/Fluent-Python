# example - sentence.py: A sentence as a sequence of words

import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        # re.findall returns a list with all non-overlapping matches of the regular expression as a list of strings
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        # self.words holds the result of .findall, so we simply return the word at the given index
        return self.words[index]

    def __len__(self):
        # To complete the sequence protocols, we implement __len__ - but it is NOT NEEDED to make an iterable object
        return len(self.words)

    def __repr__(self):
        # reprlib.repr is a utility function to generate abbreviated string representations of data structures that can be very large
        return f'Sentence({reprlib.repr(self.text)})'