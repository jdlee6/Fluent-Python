'''
Text Versus Bytes
'''

'''
Character issues

"string" is a sequence of characters
"character" - Unicode character
    a. its code point is a number from 0 to 1,114,111 (letter A is U+0041, Euro sign is U+20AC ...)
    b. actual bytes that represent a character depend on the ENCODING in use
        i. encoding is an algorithm that converts code points to byte sequences and vice-versa
            example: A (U+0041) is encoded as a the single byte \x41 in UTF-8
                            Euro Sign (U+20AC) becomes three bytes in UTF-8 \xe2\x82\xac
** converting from code points to byte is ENCODING
** converting from bytes to code points is DECODING
'''

# # str 'café' has 4 Unicode characters
# s = 'café'
# print(len(s))
# # 4

# # Encode str to bytes using UTF-8 encoding
# b = s.encode('utf-8')
# print(b)
# # bytes literals start with a b prefix
# # b'caf\xc3\xa9'

# # bytes b has 5 bytes (the code point for é is encoded as two bytes)
# print(len(b))
# # 5

# # decode bytes to str using UTF-8 encoding
# print(b.decode('utf8'))
# # café

#####################################################################
'''
Byte Essentials

immutable bytes type vs. mutable bytearray 
each item in bytes or bytearray is an integer from 0 to 255
a slice of a binary sequence ALWAYS produce a binary sequence of the same type - including slices of length 1

Three different displays:
1. for bytes in the printable ASCII range - ASCII character is used
2. for bytes to tab, newline ... the escape sequences are used
3. every other byte - a hexadecimal escape sequence is used (\x00 is null byte)
'''

# # bytes can be built from a str, given an encoding
# cafe = bytes('café', encoding='utf_8')
# print(cafe)
# # b'caf\xc3\xa9'

# # each item is an integer in range(256)
# # returns one item
# print(cafe[0])
# # 99

# # slices of bytes are also bytes - even slices of a single byte
# # returns a sequence of the same type
# print(cafe[:1])
# # b'c'

# # there is no literal syntax for bytearray: they are shown as bytearray() with a bytes literal as argument
# cafe_arr = bytearray(cafe)
# print(cafe_arr)
# # bytearray(b'caf\xc3\xa9')

# # a slice of bytearray is also a bytearray
# print(cafe_arr[-1:])
# # bytearray(b'\xa9')

# # You can use string methods with binary sequences and re module works with binary sequences as well

# # binary sequences have a class method: fromhex() 
# a = bytes.fromhex('31 4B CE A9')
# print(a)
# # b'1K\xce\xa9'

'''
building bytes or bytearray instances by calling their constructors with:
1. str and encoding keyword argument
2. iterable (0 to 255)
3. single integer (create binary sequence)
4. object that implements buffer protocol (ALWAYS copies bytes from source object to the newly created binary sequence)
    ** unlike memoryview objects which let you share memory between binary data structures
'''

# import array
# # typecode 'h' creates an array of short integers (16 bits)
# numbers = array.array('h', [-2, -1, 0, 1, 2])
# # octets holds a copy of the bytes that make up numbers
# octets = bytes(numbers)
# print(octets)
# # 10 bytes that represent the five short integers
# # b'\xfe\xff\xff\xff\x00\x00\x01\x00\x02\x00'


#####################################################################

''' 
Structs and memory views

struct module provides functions to parse packed bytes into a tuple of fields of different types 
and to perform the opposite conversion, from a tuple into packed bytes (used with bytes, bytearray and memoryview objects)
'''
# # example: using memoryview and struct to inspect a GIF image header
# import struct

# # https://docs.python.org/3/library/struct.html
# # struct format: < little-endian; 3s3s two sequence of 3 bytes; HH two 16 bit integers
# # little endian is an order in which the little end (least significant value in the sequence) is stored first
# fmt = '<3s3sHH'
# with open('filter.gif', 'rb') as fp:
#     # create memoryview from file contents in memory...
#     img = memoryview(fp.read())

# # ... then another memoryview by slicing the first one; no bytes are copied here
# header = img[:10]
# # convert to bytes for display only; 10 bytes are copied here
# print(bytes(header))
# # b'GIF89a+\x02\xe6\x00'

# # unpack memoryview into tuple of: type, version, width, and height
# print(struct.unpack(fmt, header))
# # (b'GIF', b'89a', 555, 230)

# # delete references to release the memory associated with the memoryview instances
# del header
# del img

#####################################################################

'''
Basic encoders/decoders

open(), str.encode(), bytes.decode() etc...
'utf-8', 'utf8', 'U8' (encoding arguments)
UTF encodings are designed to handle every Unicode code point

*some characters cannot be represented in certain encodings*
'''

# for codec in ['latin_1', 'utf_8', 'utf_16']:
#     print(codec, 'El Niño'.encode(codec), sep = '\t')
# # latin_1 b'El Ni\xf1o'
# # utf_8   b'El Ni\xc3\xb1o'
# # utf_16  b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'

'''
latin1 aka iso 8859_1: important because it is the basis for the other encodings
cp1252: latin1 superset by Microsoft 
cp437: original character set of IBM PC (incompatible with latin1)
gb2312: widely deployed multi-byte encodings for Asian languages
utf-8: most common 8-bit encoding on the Web 
utf-16le: support codepoints beyond U+FFFF; UTF-16 16-bit encoding scheme 
'''

#####################################################################

'''
Understanding encode/decode problems

UnicodeDecodeError (reading binary sequences into str); UnicodeEncodeError (convert str to binary sequences)
'''

# Coping with UnicodeEncodeError

# text to bytes: if character is NOT defined in the target encoding, UnicodeEncodeError

# city = 'São Paulo'
# # the 'utf_?' encodings handle any str
# print(city.encode('utf_8'))
# # b'S\xc3\xa3o Paulo'

# print(city.encode('utf_16'))
# # b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'

# # 'iso8859_1' also works for the string
# print(city.encode('iso8859_1'))
# # b'S\xe3o Paulo'

# # 'cp437' can't encode the ã which raises the UnicodeEncodeError
# # print(city.encode('cp437'))
# # # UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in position 1: character maps to <undefined>

# # the error='ignore' handler silently skips the character(s) that cannot be encoded; BAD IDEA
# print(city.encode('cp437', errors='ignore'))
# # b'So Paulo'

# # When encoding, error='replace' substitutes unencodable characters with '?'' data is lost, but users will know something is amiss
# print(city.encode('cp437', errors='replace'))
# # b'S?o Paulo'

# # 'xmlcharrefreplace' replaces unencodable characters with a XML entity
# print(city.encode('cp437', errors='xmlcharrefreplace'))
# # b'S&#227;o Paulo'

'''
Coping with UnicodeDecodeError

Not every byte sequence is valid UTF-8 or UTF-16 so when you assume one of these encodings while converting
binary sequence to text, you will get a UnicodeDecodeError if unexpected bytes are found

*legacy 8-bit encodings ('cp1252', 'iso8859_1', 'koi8_r') are able to decode any stream of bytes without errors
*if program assumes wrong 8-bit encoding -> decode garbage
'''

# # these bytes are characters for "Montréal" encoded as latin1
# octets = b'Montr\xe9al'

# # decoding with 'cp1252' (proper subset of latin1 which is why it works)
# print(octets.decode('cp1252'))
# # Montréal

# # intended for Greek which is why this is misinterpreted but no errors
# print(octets.decode('iso8859_7'))
# # Montrιal

# # KOI8-R is for Russian
# print(octets.decode('koi8_r'))
# # MontrИal

# # utf-8 codec detects that this is not a valid UTF-8
# # print(octets.decode('utf-8'))
# # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation bytes

# # using 'replace' error handling, the error gets replaced with the Unicode REPLACEMENT CHARACTER �
# # which represents unknown characters
# print(octets.decode('utf_8', errors='replace')) 
# # Montr�al


#####################################################################

'''
SyntaxError when loading modules with unexpected encoding

if you load a .py module containing non-UTF-8 data and no encoding declaration:

SyntaxError: Non-UTF-8 code starting with '\xe1' in file ola.py on line
1, but no encoding declared; see http://python.org/dev/peps/pep-0263/
for details

**to fix these syntax errors: add a magic coding comment at the top of the file
*default encoding for python3 is utf-8
'''

# example

# coding: cp1252
# print('Olá, Mundo!')


#####################################################################

'''
Discover encoding of a byte sequence (Can't)

Chardet (Python Library)

$ chardetect 04-text-byte.asciidoc
04-text-byte.asciidoc: utf-8 with confidence 0.99

BOM - byte order mark
'''

# u16 = 'El Niño'.encode('utf_16')
# print(u16)
# # b'\xff\xfe' = BOM denoting "little endian" byte ordering
# # b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'

'''
remember that on a little endian machine, for each code point the least significant byte comes first: 
the letter E code point U+0045 (decimal 69) is encoded in byte offsets 2 and 3 as 69 and 0:

on a big endian CPU, the encoding would be reversed:
E would come be encoded as 0 and 69

**note: [255, 254 . . .] represents the b'\xff\xfe' in a L.E. system
'''

# print(list(u16))
# [255, 254, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]


# # Notice how a BOM is not generated here because it is EXPLICITLY little endian
# u16le = 'El Niño'.encode('utf_16le')
# print(list(u16le))
# # [69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]

# # if you specify which endian, a BOM is not generated
# u16be = 'El Niño'.encode('utf_16be')
# print(list(u16be))
# # [0, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111]


#####################################################################


# Handling Text Files

# Unicode sandwich 
# 1. bytes to str (early as possible)
# 2. body should be in str
# 3. str to bytes (late as possible)

# print(open('cafe.txt', 'w', encoding='utf_8').write('café'))
# # 4

# # not on my machine but for example Python assumes the wrong system default encoding and the é is failed to be decoded
# # doesn't show on Linux bc their default encoding is UTF-8
# print(open('cafe.txt').read())
# # 'cafÃ©'


# fp = open('cafe.txt', 'w', encoding='utf_8')
# # by default, open operates in text mode and returns a TextIOWrapper object
# print(fp)
# # <_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>

# # the write method on a TextIOWrapper returns the number of Unicode characters written
# print(fp.write('café'))
# # 4
# fp.close()

# import os
# # os.stat reports that the file holds 5 bytes; UTF-8 encodes 'é' as two bytes
# print(os.stat('cafe.txt').st_size)
# # 5

# # no explicity encoding returns a TextIOWrapper with encoding set to system default (UTF-8)
# fp2 = open('cafe.txt')
# print(fp2)
# # <_io.TextIOWrapper name='cafe.txt' mode='r' encoding='UTF-8'>

# print(fp2.encoding)
# # UTF-8

# print(fp2.read())
# # café

# # open file with Windows encoding cp1252
# fp3 = open('cafe.txt', encoding='cp1252')
# # byte 0xc3 and 0xa9 are Ã©
# print(fp3.read())
# # cafÃ©

# # 'rb' flag opens a file for reading in binary mode
# fp4 = open('cafe.txt', 'rb')
# print(fp4)
# # <_io.BufferedReader name='cafe.txt'>

# # reading this file returns bytes (as expected)
# print(fp4.read())
# # b'caf\xc3\xa9'

#####################################################################


# Encoding defaults: a madhouse

# Example: exploring encoding defaults

# import sys, locale

# expressions = '''
#             locale.getpreferredencoding() 
#             type(my_file)
#             my_file.encoding
#             sys.stdout.isatty()
#             sys.stdout.encoding
#             sys.stdin.isatty()
#             sys.stdin.encoding
#             sys.stderr.isatty()
#             sys.stderr.encoding
#             sys.getdefaultencoding()
#             sys.getfilesystemencoding()
# '''

# # isatty() returns Boolean if file is connected with a terminal device
# # sys.stdin is another way to read the file object ( correlated with input() )
# # sys.stderr are for exceptions
# # sys.stdout ( correlated with print() )
# # sys.getdefaultencoding() used to convert binary to and from str
# # sys.getfilesystemencoding() used to encode/decode filenames

# my_file = open('dummy', 'w')

# for expression in expressions.split():
#     value = eval(expression)
#     print(expression.rjust(30), '->', repr(value))

# locale.getpreferredencoding() is the MOST important setting (default for opening text files)
# Text files (my_file) use locale.getprefferedencoding()
# sys.stdin.isatty() is True if the output is going to the console
# it would return False if the it being redirected to another file

# #  locale.getpreferredencoding() -> 'UTF-8'
# #                            type(my_file) -> <class '_io.TextIOWrapper'>
# #                      my_file.encoding -> 'UTF-8'
# #                      sys.stdout.isatty() -> True
# #                   sys.stdout.encoding -> 'UTF-8'
# #                        sys.stdin.isatty() -> True
# #                     sys.stdin.encoding -> 'UTF-8'
# #                       sys.stderr.isatty() -> True
# #                    sys.stderr.encoding -> 'UTF-8'
# #           sys.getdefaultencoding() -> 'utf-8'
# #       sys.getfilesystemencoding() -> 'utf-8'


#####################################################################


# Normalizing Unicode for saner comparisons

# s1 = 'café'
# # \u0301 is the COMBINING ACUTE ACCENT
# s2 = 'cafe\u0301'
# print(s1, s2)
# # café café

# print(len(s1))
# # 4
# print(len(s2))
# # 5

# print(s1 == s2)
# # False

# Python sees two different sequences of code points and considers them not equal
# which is why we need to use unicodedata.normalize() function
# first argument is of the four: 'NFC', 'NFD', 'NFKC', 'NFKD'

# NFC - composes code points to produce the shortest equivalent string (normalizaton form recommended by W3C)
# NFD - decomposes, expanding composed characters into base and separate characters

# from unicodedata import normalize
# # composed "e" with acute accent
# s1 = 'café' 
# # decomposed "e" and acute accent
# s2 = 'cafe\u0301'
# print(len(s1), len(s2))
# # 4 5
# print(len(normalize('NFC', s1)), len(normalize('NFC', s2)))
# # 4 4
# print(len(normalize('NFD', s1)), len(normalize('NFD', s2)))
# # 5 5
# print(normalize('NFC', s1) == normalize('NFC', s2))
# # True
# print(normalize('NFD', s1) == normalize('NFD', s2))
# # True

# Some are visually identical but compare unequal (ohm and omega character)

# from unicodedata import normalize, name
# ohm = '\u2126'
# print(name(ohm))
# # OHM SIGN

# ohm_c = normalize('NFC', ohm)
# print(name(ohm_c))
# # GREEK CAPITAL LETTER OMEGA

# print(ohm == ohm_c)
# # False

# print(normalize('NFC', ohm) == normalize('NFC', ohm_c))
# # True

# Letter K in NFKC and NFKD stand for "compatibility"
# each compatibility character is replaced by "compatibilty decomposition"
'''
reference to ch4. (this version has errors)
'''

# from unicodedata import normalize, name

# half = '1⁄2'
# print(normalize('NFKC', half))
# # 1⁄2

# four_squared = '42'
# print(normalize('NFKC', four_squared))
# # 42

# micro = 'μ'
# micro_kc =  normalize('NFKC', micro)
# print(micro, micro_kc)
# # μ μ

# print(ord(micro), ord(micro_kc))
# # 181 956

# print(name(micro), name(micro_kc))
# # ('MICRO SIGN', 'GREEK SMALL LETTER MU')

# making the conversions changes the meaning therefore NFKC or NFKD may lose or distory information
# transformations may cause data loss


#####################################################################

# Case Folding

# converting all text to lowercase with additional transformations ( str.casefold() )

# from unicodedata import normalize, name

# '''
# problem: why does python think that they are both GREEK SMALL LETTER MU 
# '''
# micro = 'μ'
# print(name(micro))
# # GREEK SMALL LETTER MU

# micro_cf = micro.casefold()
# print(name(micro_cf))
# # GREEK SMALL LETTER MU

# print(micro, micro_cf)
# # μ μ

# eszett = 'ß'
# print(name(eszett))
# # LATIN SMALL LETTER SHARP S

# eszett_cf = eszett.casefold()
# print(eszett, eszett_cf)
# # ß ss


#####################################################################

'''
Utility functions for normalized text matching
str.casefold() - for case-insensitive comparisons

Using Normal Form C, case sensitive:

s1 = 'café'
s2 = 'cafe\u0301'
s1 == s2
# False
nfc_equal(s1, s2)
# True
nfc_equal('A', 'a')
# False


Using Normal Form C with case folding:
s3 = 'Straße'
s4 = 'strasse'
s3 == s4
# False
nfc_equal(s3, s4)
# False
fold_equal(s3, s4)
# True
fold_equal(s1, s2)
# True
fold_equal('A', 'a')
# True
'''
# from unicodedata import normalize

# def nfc_equal(str1, str2):
#     return normalize('NFC', str1) == normalize('NFC', str2)

# def fold_equal(str1, str2):
#     return (normalize('NFC', str1).casefold() == 
#                 normalize('NFC', str2).casefold())


'''
Extreme "normalization": taking out diacritics

To remove all diacritics from a str: look at the example below
'''
# import unicodedata, string

# def shave_marks(txt):
#     ''' Remove all diacritic marks '''
#     # decompose all characters into BASE characters and combining marks
#     norm_txt = unicodedata.normalize('NFD', txt)
#     shaved = ' '.join(c for c in norm_txt
#                                 # filter out all combining marks
#                                 if not unicodedata.combining(c))
#     # recompose all characters
#     return unicodedata.normalize('NFC', shaved)


# # examples using shave_marks
# # shave_marks also changes non-Latin characters which will never become ASCII just by losing their accents

# order = '“Herr Voß: • 1⁄2 cup of ŒtkerTM caffè latte • bowl of açaí.”'
# # Only the letters “è”, “ç” and “í” were replaced.
# print(shave_marks(order))
# # “ H e r r   V o ß :   •   1 ⁄ 2   c u p   o f   Œ t k e r T M   c a f f e   l a t t e   •   b o w l   o f   a c a i . ”
# Greek = 'Ζέφυρος, Zéfiro'
# # Both “έ” and “é” were replaced.
# print(shave_marks(Greek))
# # Ζ ε φ υ ρ ο ς ,   Z e f i r o

# # it makes sense to analyze base character and remove attached marks only if the base character is a letter from the Latin alphabet (example below)
# def shave_marks_latin(txt):
#     ''' 
#     remove all diacritic marks from latin base characters
#     '''
#     # Decompose all characters into base characters and combining marks
#     norm_txt = unicodedata.normalize('NFD', txt)
#     latin_base = False
#     keepers = []
#     for c in norm_txt:
#         # skip over combining marks when base character is Latin
#         if unicodedata.combining(c) and latin_base:
#             # ignore diacritic on Latin base char
#             continue
#         # Otherwise, keep current character
#         keepers.append(c)
#         # if it isn't combining char, it's a new base char
#         # detect new base and determine if it's Latin
#         if not unicodedata.combining(c):
#             latin_base = c in string.ascii_letters
#     shaved = ' '.join(keepers)
#     # recompose all characters
#     return unicodedata.normalize('NFC', shaved)


# # Example: Transform some Western typographical symbols into ASCII  (this example is part of def shave_marks() example)
# # Build mapping table for char to char replacement
# single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–— ̃›""",
#                                             """'f"*^<''""---~>""")
# # Build mapping table for char to string replacement
# multi_map = str.maketrans({
#             '€': '<euro>',
#             '...': '...',
#             'Œ': 'OE',
#             'TM': '(TM)',
#             'œ': 'oe',
#             '‰': '<per mille>',
#             '‡': '**',
# })

# # merge mapping tables
# multi_map.update(single_map)

# # dewinize does not affect ASCII or latin1 text, only the Microsoft additions to latin1 in cp1252
# def dewinize(txt):
#     ''' 
#     Replace Win1252 symbols with ASCII chars or sequences
#     '''
#     return txt.translate(multi_map)

# def asciize(txt):
#     # apply dewinize and remove diacritical marks
#     no_marks = shave_marks_latin(dewinize(txt))
#     # replace the eszett with 'ss' (we are no using case fold here because we want to preserve the case)
#     no_marks = no_marks.replace('ß', 'ss')
#     # apply NFKC normalization to compose characters with their compatibility code points
#     return unicodedata.normalize('NFKC', no_marks)


# # Examples the use asciize

# order = '“Herr Voß: • 1⁄2 cup of ŒtkerTM caffè latte • bowl of açaí.”'
# # dewinize replaces curly quotes, bullets, and TM (trade mark symbol)
# print(dewinize(order))
# # '"Herr Voß: - 1⁄2 cup of OEtker(TM) caffè latte - bowl of açaí."'

# # asciize applies dewinize, drops diacritics and replaces the 'ß'
# print(asciize(order))
# # '"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."'

# # summary: the functions above perform deep surger on the text with a good chance of changing its meaning


#####################################################################


# Sorting Unicode text

# fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
# # Sorting rules vary for different locales - accents and cedillas rarely make a difference when sorting
# print(sorted(fruits))
# ['acerola', 'atemoia', 'açaí', 'caju', 'cajá']

# The list should be: ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']

# locale.strxfrm() - transforms a string to one that can be used in locale-aware comparisons
# setlocale(LC_COLLATE, <<your_locale>>) before using locale.strxfrm

# import locale

# print(locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8'))
# # 'pt_BR.UTF-8'
# fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
# sorted_fruits = sorted(fruits, key=locale.strxfrm)
# print(sorted_fruits)
# # ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']

'''
1. locale settings are global and calling setlocale in a library is not recommended
2. locale must be installed on the OS otherwise setlocale raises a locale.Error: unsupported locale setting
3. must know how to spell the locale name
4. locale must be correctly implemented by the makers of the OS
'''

#####################################################################

'''
Sorting with the Unicode Collation Algorithm
'''
# import pyuca

# coll = pyuca.Collator()
# fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
# sorted_fruits = sorted(fruits, key=coll.sort_key)
# print(sorted_fruits)
# # ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']


'''
The Unicode database

- records whether a character is printable, is a letter, a decimal digit etc.
    i. this is how isidentifier, isprintable, isdecimal, isnumeric work
'''

# import unicodedata, re

# re_digit = re.compile(r'\d')

# sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

# for char in sample:
#     # code point in U+0000 format
#     print('U+%04x' % ord(char),
#             # character centralized in a str of length 6
#             char.center(6),
#             # show re_dig if character matches the r'\d' regex
#             're_dig' if re_digit.match(char) else '-',
#             # show isdig if char.isdigit() is True
#             'isdig' if char.isdigit() else '-',
#             # show isnum if char.isnumeric() is True
#             'isnum' if char.isnumeric() else '-',
#             # Numeric value formatted with width 5 and 2 decimal places
#             format(unicodedata.numeric(char), '5.2f'),
#             # unicode character name
#             unicodedata.name(char),
#             sep='\t')

# U+0031    1     re_dig  isdig   isnum    1.00   DIGIT ONE
# U+00bc    ¼     -       -       isnum    0.25   VULGAR FRACTION ONE QUARTER
# U+00b2    ²     -       isdig   isnum    2.00   SUPERSCRIPT TWO
# U+0969    ३     re_dig  isdig   isnum    3.00   DEVANAGARI DIGIT THREE
# U+136b    ፫     -       isdig   isnum    3.00   ETHIOPIC DIGIT THREE
# U+216b    Ⅻ     -       -       isnum   12.00   ROMAN NUMERAL TWELVE
# U+2466    ⑦     -       isdig   isnum    7.00   CIRCLED DIGIT SEVEN
# U+2480    ⒀     -       -       isnum   13.00   PARENTHESIZED NUMBER THIRTEEN
# U+3285    ㊅    -       -       isnum    6.00   CIRCLED IDEOGRAPH SIX

# The 6th column is the result of calling unicodedata.numeric(char) on the character

#####################################################################


'''
Dual mode str and bytes

str vs. bytes in regex
1. if building regular expression with bytes, patterns such as \d and \w match ASCII characters
2. in contrast, if these patterns are given as str - they match Unicode digits or letters beyond ASCII
'''

# import re

# # the first two regular expression are of the str type
# re_numbers_str = re.compile(r'\d+')
# re_words_str = re.compile(r'\w+')

# # the last two are of the bytes type
# re_numbers_bytes = re.compile(rb'\d+')
# re_words_bytes = re.compile(rb'\w+')

# # Unicode text to search containing the Tamil digits for 1729 (logical line continues until the right parenthesis token)
# text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"
#                     # This string is joined to the previous one at compile time
#                   " as 1729 = 13 + 123 = 93 + 103.")

# text_bytes = text_str.encode('utf-8')

# print('Text', repr(text_str), sep='\n')
# print('Numbers')
# # the str pattern r'\d+' matches the Tamil and ASCII digits
# print(' str :', re_numbers_str.findall(text_str))
# # the bytes pattern rb'\d+' matches only the ASCII bytes for digits
# print(' bytes: ', re_numbers_bytes.findall(text_bytes))
# print('Words')
# # the str patttern r'\w+' matches the letters, superscripts, Tamil and ASCII digits
# print(' str :', re_words_str.findall(text_str))
# # the bytes pattern rb'\w+' matches only the ASCII bytes for letters and digits
# print(' bytes:', re_words_bytes.findall(text_bytes))

# # Text
# # 'Ramanujan saw ௧௭௨௯ as 1729 = 13 + 123 = 93 + 103.'
# # Numbers
# #  str : ['௧௭௨௯', '1729', '13', '123', '93', '103']
# #  bytes:  [b'1729', b'13', b'123', b'93', b'103']
# # Words
# #  str : ['Ramanujan', 'saw', '௧௭௨௯', 'as', '1729', '13', '123', '93', '103']
# #  bytes: [b'Ramanujan', b'saw', b'as', b'1729', b'13', b'123', b'93', b'103']


# Another important dual module is the os module

'''
str versus bytes on os functions

filenames may be byte sequences which may NOT be valid and CANNOT be decoded to str
os module functions accept file names or path names take arguments as str or bytes

sys.getfilesystemencoding() is used when one function is called with a str argument and the OS response will decode the same codec
you can pass bytes arguments to the os functions to get the bytes return values (lets you deal with ANY filename)

fsencode(filename) - encodes filenames (str or bytes) to bytes
fsdecode(filename) - decodes filename (str or bytes) to str 

Unix platforms - surrogateescape error handler (deals with unexpected bytes or unknown encodings)
Windows - strict error handler
'''

# import os

# # the second filename is "digits-of-π.txt"
# print(os.listdir('.'))
# # ['abc.txt', 'digits-of-π.txt']

# # Given a byte argument, listdir returns filenames as bytes (UTF-8)
# print(os.listdir(b'.'))
# # [b'abc.txt', b'digits-of-\xcf\x80.txt']


# import os 

# # list directory with a non ASCII file name
# print(os.listdir('.'))
# # ['abc.txt', 'digits-of-π.txt']

# # Let's pretend we don't know the encoding and get file names as bytes
# print(os.listdir(b'.'))
# # [b'abc.txt', b'digits-of-\xcf\x80.txt']

# # pi_name_bytes is the filename with pi character
# pi_name_bytes = os.listdir(b'.')[1]

# # Decode it to str using the 'ascii' codec with 'surrogateescape'
# pi_name_str = pi_name_bytes.decode('ascii', 'surrogateescape')

# # Each non-ASCII byte is replaced by a surrogate code point: '\xcf\x80'
# # becomes '\udccf\udc80'
# print(pi_name_str)
# # 'digits-of-\udccf\udc80.txt'

# # Encode back to ASCII bytes: each surrogate code point is replaced by the byte it replaced
# print(pi_name_str.encode('ascii', 'surrogateescape'))
# # b'digits-of-\xcf\x80.txt'