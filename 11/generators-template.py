"""
Turn the following unix pipeline into Python code using generators

$ for i in ../*/*py; do grep ^import $i|sed 's/import //g' ; done | sort | uniq -c | sort -nr
   4 unittest
   4 sys
   3 re
   3 csv
   2 tweepy
   2 random
   2 os
   2 json
   2 itertools
   1 time
   1 datetime
"""
from __future__ import print_function
import collections
import glob
import itertools
import re


def expand_wildcard(wildcard):
    """
    Given a wildcard, yield a sequence of matching file names
    """
    return glob.iglob(wildcard)


def lines_from_paths(paths):
    """
    Given a number of paths, yield a sequence of lines
    """
    for path in paths:
        with open(path) as f:
            for line in f:
                yield line.rstrip('\n')


def grep(string_list, pattern):
    """
    Given a sequence of strings and a pattern, yield a list of matching
    strings
    """
    pattern = re.compile(pattern)
    for line in string_list:
        if re.search(pattern, line):
            yield line


def search_and_replace(strings_list, search_term, new_term):
    for line in strings_list:
        new_line = line.replace(search_term, new_term)
        yield new_line

def count_adjacent(iterable):
    """
    Given a sequence of elements, yield a sequence of (count, element)

    >>> list(count_semilar(['a', 'a', 'a', 'b', 'c', 'c']))
    [(3, 'a'), (1, 'b'), (2, 'c')]
    """
    for element, elements_group in itertools.groupby(iterable):
        yield len(tuple(elements_group)), element


if __name__ == "__main__":
    print('\n--- Count using itertools.groupby')
    files = expand_wildcard('../*/*.py')
    lines = lines_from_paths(files)
    lines = grep(lines, r'^import')
    lines = search_and_replace(lines, 'import ', '')
    lines = sorted(lines)
    count_and_names = count_adjacent(lines)
    count_and_names = sorted(count_and_names, reverse=True)
    print('\n'.join('{} {}'.format(count, name)
        for count, name in count_and_names))

    print('\n--- Count using collections.Counter')
    files = expand_wildcard('../*/*.py')
    lines = lines_from_paths(files)
    lines = grep(lines, r'^import')
    lines = search_and_replace(lines, 'import ', '')
    counter = collections.Counter(lines)
    print('\n'.join('{} {}'.format(count, name)
        for name, count in counter.most_common()))


