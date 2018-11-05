import six
from tests.aho_corasick import test as aho_corasick_test
from tests.enriching import test as enricher_test


def test():
    aho_corasick_test()
    enricher_test()


if __name__ == '__main__':
    test()
