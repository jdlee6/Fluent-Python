# itertools.cycle is similar to a while loop that lasts forever

import itertools, time

for i in itertools.cycle('ABC'):
    print(i, end=' ')
