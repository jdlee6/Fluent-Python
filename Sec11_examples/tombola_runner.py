import doctest, abc, sys
from tombola import Tombola

# modules containing real or virtual subclasses of Tombola for testing
import lotto, tombolist

# reStructuredText (rst) file format for textual data used primarily in Python
TEST_FILE = 'tombola_tests.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed -{2}'

def main(argv):
    verbose = '-v' in argv
    # __subclasses__() lists the direct descendants that are alive in memory. that's why we imported the modules to test, even if there is no further mention of them in the source code: to load the classes into memory
    real_subclasses = Tombola.__subclasses__()
    # print(real_subclasses)

    # Python3.7 does NOT support _abc_registry
    # virtual_subclasses = list(Tombola._abc_registry)
    # abc._get_dump(Tombola) --> returns a 4-tuple of (_abc_registry, _abc_cache, _abc_negative_cache, _abc_negative_cache_version)
    
    # index the _abc_registry in abc._get_dump and build a list so we can concatenate with the result of __subclasses__()
    virtual_subclasses = [
        ref() for ref in abc._get_dump(Tombola)[0] if ref()
    ]
    # print(virtual_subclasses)

    # iterate over the subclasses found, passing each to the test function
    for cls in real_subclasses + virtual_subclasses:
        test(cls, verbose)

def test(cls, verbose=False):
    # doctest.testfile(filename, module_relative=True, name=None, package=None, globs=None . . . )
    res = doctest.testfile(
        TEST_FILE,
        # the cls argument - class to be tested - is bound to the name ConcreteTombola in the global namespace provided to run the doctest
        globs={'ConcreteTombola':cls},
        verbose=verbose,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
    )
    tag = 'FAIL' if res.failed else 'OK'
    # The test result is printed with the name of the class, the number of tests attempted, tests failed and an 'OK' or 'FAIL' label
    print(TEST_MSG.format(cls.__name__, res, tag))

if __name__ == "__main__":
    main(sys.argv)



# LotteryBlower     0 tests,  0 failed -OK
# TomboList         0 tests,  0 failed -OK