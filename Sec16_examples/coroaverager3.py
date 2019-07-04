# example - using yield from to drive averager and report statistic

'''
caller (main) ---> sends to subgenerator (averager)
    -throws and closes to 
subgenerator (averager) yields to ---> caller (main)
subgenerator (averager) raises StopIteration to ---> delegating generator (grouper)
'''

from collections import namedtuple

Result = namedtuple('Result', 'count average')

# the subgenerator - generator obtained from the <iterable> part of the yield from expression
# same averager coroutine from the previous example but in this example it acts as the subgenerator
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        # each value sent by the client code in main will be bound to term here
        term = yield
        # the crucial terminating condition. Without it, a yield from calling this coroutine will block forever
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    # the returned Result will be the value of the yield from expression in grouper
    return Result(count, average)

# the delegating generator - the generator function that contains the yield from <iterable> expression
# grouper is the delgating generator
def grouper(results, key):
    # each iteration in this loop creates a new instance of averager; each is a generator object operating as a coroutine
    while True:
        # Whenever grouper is sent a value, it's piped into the averager instance by the yield from. grouper will be suspended here as long as the averager instance is consuming values sent by the client. When an averager instance runs to the end, the value it returns is bound to results[key]. The while loop then proceeds to create another averager instance
        results[key] = yield from averager()

# the caller aka the client code
# main is the client code, or "caller" in PEP 380 parlance. This is the function that drives everything
def main(data):
    results = {}
    for key, values in data.items():
        # group is a generator object resulting from calling grouper with the results dict to collect the results, and a particular key. It will operate as a coroutine
        group = grouper(results, key)
        # prime the coroutine
        next(group)
        for value in values:
            # send each value into the grouper. that value ends up in the term = yield line of averager; grouper never has a chance to see it
            group.send(value)
        # Sending None into grouper causes the current averager instance to TERMINATE and allows grouper to run again, which creates another averager for the next group of values
        # IMPORTANT! - this line of code TERMINATES one averager and starts the next; if this line is commented out then the script produces NO output
        group.send(None)

    # print(results)
    report(results)

# output report

def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))

data ={
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == "__main__":
    main(data)

#  9 boys  averaging 40.42kg
#  9 boys  averaging 1.39m
# 10 girls averaging 42.04kg
# 10 girls averaging 1.43m


'''
explanation of what would happen if we didn't call the group.send(None) in main()
    -Each iteration of the outer for loop creates a new grouper instance named group; this is the delegating generator
    -The call next(group) primes the grouper delegating generator, which enters its while True loop and suspends at the yield from, after calling the subgenerator averager
    -The inner for loop calls group.send(value); this feeds the subgenerator averager directly. Meanwhile, the current group instance of grouper is suspended at the yield from
    -When the inner for loop ends, the group instance is still suspended at the yield from, so the assignment to results[key] in the body of grouper has not happened yet
    -without the last group.send(None) in the outer for loop, the averager subgenerator NEVER terminates, the delegating generator group is never reactivated, and the assignment to results[key] never happens
    -when execution loops back to the top of the outer for loop, a new grouper instance is created and bound to group. The previous grouper instance is garbage collected (together with its own unfinished averager subgenerator instance)

**if a subgenerator NEVER terminates, the delegating generator will be suspended FOREVER at the "yield from"
'''
