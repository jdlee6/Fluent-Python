import time, sys

# this prints it all the values at the same time
for i in range(5):
    print(i, end=' ')
    time.sleep(.3)

print('\ntesting flush')
time.sleep(3)

# this prints the values one by one on each iteration
for i in range(5):
    print(i, end=' ')
    sys.stdout.flush()
    time.sleep(.3)
