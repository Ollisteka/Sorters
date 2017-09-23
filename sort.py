#!/usr/bin/env python3
import argparse
import json
import os
import sys
from time import time

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.comparison_functions import less, greater
from logic.sort_functions import merge_sort, shell_sort, bubble_sort, hoare_sort, radix_sort

COMP_NUM = "Number of comparisons:"
PERM_NUM = "Number of permutations:"


class Timer:
    def __init__(self, message=None):
        self.message = message
        self.total_ms = 0
        self.total_sec = 0
        self.total_min = 0
        self.total_hours = 0

    def __enter__(self):
        self.start = time()
        # could return anything, to be used like this: with Timer("Message") as
        # value:
        return self

    def __exit__(self, type, value, traceback):
        self.total_sec = (time() - self.start)
        self.total_min = self.total_sec / 60
        self.total_hours = self.total_min / 60
        self.total_ms = self.total_sec * 1000
        # self.print_results()

    def start(self):
        self.__enter__()

    def stop(self):
        self.__exit__()

    def print_results(self):
        """
        Function counts and displays the results of timer ticks
        :return:
        """
        print("Total sec: ", self.total_sec)
        print("Total min: ", self.total_min)
        print("Total hours: ", self.total_hours)


def write_json_in_file(filename, data, encoding="utf-8"):
    """
    Write list into file, using json
    :param encoding: str
    :type filename: str
    :param data:
    :return:
    """
    with open(filename, "w", encoding=encoding) as f:
        f.write(json.dumps(data))


def read_json_file(filename, encoding):
    """
    Read data, written in a json format from a file, and return it
    :param encoding: str
    :param filename: str
    :return:
    """
    with open(filename, "r", encoding=encoding) as file:
        return json.loads(file.read())


def sort(smth_to_sort, sort_func, reverse=False, cmp=None):
    """
    Sort something, using specific sort function.
    :param smth_to_sort:
    :param sort_func:
    :param reverse:
    :param cmp:
    :return:
    """
    if sort_func is not radix_sort:
        return sort_func(
            smth_to_sort,
            reverse=reverse,
            cmp=eval(cmp) if cmp is not None else cmp)
    else:
        try:
            return radix_sort(smth_to_sort, reverse=reverse)
        except TypeError as e:
            print("Error: only integer and float numbers can be sorted using radix sort.")


def find_result(args, data):
    if args.merge:
        return sort(data, merge_sort, args.reverse, args.cmp)
    elif args.shell:
        return sort(data, shell_sort, args.reverse, args.cmp)
    elif args.hoare:
        return sort(data, hoare_sort, args.reverse, args.cmp)
    elif args.bubble:
        return sort(data, bubble_sort, args.reverse, args.cmp)
    elif args.radix:
        return sort(data, radix_sort, args.reverse, args.cmp)
    else:
        sys.exit("Error: sort algorithm must be specified")


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(
            os.path.basename(
                sys.argv[0])),
        description='Sort something, using some algorithm')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--merge', action="store_true", dest='merge',
                       help='sort using merge algorithm')
    group.add_argument('--shell', action="store_true", dest='shell',
                       help='sort using shell algorithm')
    group.add_argument('--hoare', action="store_true", dest='hoare',
                       help='sort using hoare algorithm')
    group.add_argument('--bubble', action="store_true", dest='bubble',
                       help='sort using bubble algorithm')
    group.add_argument('--radix', action="store_true", dest='radix',
                       help='sort using radix algorithm')
    parser.add_argument('fn', metavar='FILE', type=str,
                        help='name of the file with something to sort')
    parser.add_argument('-r', '--reverse', action="store_true", dest='reverse',
                        help='sort something in reversed order')
    parser.add_argument('-k', '--key', type=str, dest='cmp',
                        help='sort something, using certain compare function')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        dest='output',
        help='choose, whether to print result on the screen, or write into file')
    parser.add_argument(
        '-c',
        '--comparisons',
        action="store_true",
        dest='comp_count',
        help='write, how many comparisons were made during sort')
    parser.add_argument(
        '-p',
        '--permutations',
        action="store_true",
        dest='perm',
        help='write, how many permutations were made during sort')
    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        dest='encoding',
        default='utf-8',
        help='choose FILE (and output file, if key -o is chosen) encoding')
    parser.add_argument('-t', '--time', action="store_true", dest='time',
                        help='check how long something was sorted')

    args = parser.parse_args()

    data = read_json_file(args.fn, args.encoding)

    if args.time:
        with Timer():
            result = find_result(args, data)
    else:
        result = find_result(args, data)

    if not args.output:
        print(result)

    if args.perm:
        print(PERM_NUM, result.permutations())
    if args.comp_count:
        if less.calls != 0:
            print(COMP_NUM, less.calls)
        else:
            print(COMP_NUM, greater.calls)


if __name__ == '__main__':
    sys.exit(main())
