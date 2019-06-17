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

