#!/usr/bin/env python3
import argparse
import os
import sys
import arrays_generator as ar_gen
from sort import read_json_file, Timer, write_json_in_file
from copy import deepcopy
from pprint import pprint
from sys import platform
from collections import defaultdict
import csv

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.comparison_functions import less, greater
from logic.sort_functions import merge_sort, shell_sort, bubble_sort, hoare_sort, radix_sort


ARRAYS = ar_gen.ARRAYS
TIME = "TIME"
SIZE = "SIZE"
PERMUTATIONS = "PERM"
COMPARISONS = "COMP"
SORT_FUNC = [merge_sort, shell_sort, bubble_sort, hoare_sort, radix_sort, sorted]
RANDOM = "RND"
BEST = "BEST"
WORST = "WORST"
CASES = [RANDOM, BEST, WORST]
STAT_CASES = [TIME, PERMUTATIONS, COMPARISONS]
LITTLE_SAMPLE = {val: 0 for val in STAT_CASES}
UNITS = {TIME: "ms", PERMUTATIONS: "Number", COMPARISONS: "Number"}


def make_result_dict(numbers):
    result = defaultdict(dict)
    for case in CASES:
        for func in SORT_FUNC:
                result[case][func.__name__] = {num: deepcopy(LITTLE_SAMPLE) for num in numbers}
    return result


def fill_result_dict(cases, result_dict, num):
    for func in SORT_FUNC:
        for case in cases:
            with Timer() as timer:
                result = func(cases[case])
            result_dict[case][func.__name__][num][TIME] = timer.total_ms
            if func.__name__ == "sorted":
                result_dict[case][func.__name__][num][PERMUTATIONS] = 0
            else:
                result_dict[case][func.__name__][num][PERMUTATIONS] = result.permutations()
            result_dict[case][func.__name__][num][COMPARISONS] = less.calls + greater.calls
            less.calls = 0
            greater.calls = 0


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS]'.format(
            os.path.basename(
                sys.argv[0])),
        description='Generate data')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--num', type=int, dest='num', nargs='+',
                        help='number of elements to be generated')
    parser.add_argument(
        '-o',
        '--output',
        action='store_true',
        dest='output',
        help='choose, whether to print result on the screen, or write into file')
    args = parser.parse_args()

    if platform.startswith("linux"):
        python = "python3"
    elif platform == "win32":
        python = "python"

    for num in args.num:
        os.system("{0} arrays_generator.py -r -w -b -o {1} -n {1}".format(python, num))

    result = make_result_dict(args.num)
    for num in args.num:
        cases = read_json_file(str(num), 'utf-8')
        fill_result_dict(cases, result, num)
    if args.output:
        write_csv_in_file(result, args.num)
    else:
        pprint(result)


def write_csv_in_file(data, nums):
    for case in CASES:
        for stat_case in STAT_CASES:
            stat = [[num]+[data[case][func.__name__][num][stat_case]for func in SORT_FUNC] for num in nums]
            header = [["Arrays' count"] + [stat_case.lower().capitalize()] * 6]
            measure = [[""] + [UNITS[stat_case]] * 6]
            functions = [[""] + [func.__name__ for func in SORT_FUNC]]
            with open(stat_case.lower() + "_" + case.lower() + ".csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerows(header)
                writer.writerows(measure)
                writer.writerows(functions)
                writer.writerows(stat)

if __name__ == '__main__':
    sys.exit(main())
