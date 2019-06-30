# example - ArithmeticProgression class

class ArithmeticProgression:
    # __init__ requires two arguments: begin and step. end is optional, which is set to None therefore the series will be unbounded
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # none -> "infinite" series

    def __iter__(self):
        # this line produces a result value equal to self.begin, but coerced to the type of subsequent additions
        # coerced to the type of begin
        # coerce() deprecated after Python2; used to be coerce(10, bad("102")) --> (102, 10)
        result = type(self.begin + self.step)(self.begin)
        # for readability, the forever flag will be True if self.end attribute is None, resulting in an unbounded series
        forever = self.end is None
        index = 0
        # this loop runs forever or until the result matches or exceeds self.end. When this loop exits, so does the function
        while forever or result < self.end:
            # the current result is produced
            yield result
            index += 1
            # the next potential result is calculated. It may never be yielded because the while loop may terminate
            result = self.begin + self.step * index

'''
note in the last line, instead of incrementing the result with self.step iteratively; we used an index variable and calculate each result by adding self.begin to self.step multiplied by index to reduce the culative effect of errors when working with floats

example of the use of a generator function to implement __iter__ special method however the class itself can be reduced to a generator function (which is a generator factory)
'''
# example - generator function that does the same job with less code
# def aritprog_gen(begin, step, end=None):
#     result = type(begin + step)(begin)
#     forever = end is None
#     index = 0
#     while forever or result < end:
#         yield result
#         index += 1
#         result = begin + step * index
