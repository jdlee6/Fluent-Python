text = "yo what the fuck bro, can, this, split, up"

print(text)
# yo what the fuck bro, can, this, split, up

print(text.replace(',', ' '))
# yo what the fuck bro  can  this  split  up

new_text = text.replace(',',' ').split()
print(new_text)
# ['yo', 'what', 'the', 'fuck', 'bro', 'can', 'this', 'split', 'up']

print(tuple(new_text))