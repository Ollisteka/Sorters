#!/usr/bin/env python3
import random
import sys
import os
import argparse
from sort import write_json_in_file
from pprint import pprint

TIME = "TIME"
ARRAYS = "arrays.json"
RANDOM = "RND"
BEST = "BEST"
WORST = "WORST"


def generate_random_array(quantity):
    return [random.randint(-9999999, 99999999) for _ in range(quantity)]


def generate_best_case_array(quantity):
    array = sorted(random.randint(-9999999, 99999999) for _ in range(quantity))
    return array


def generate_worst_case_array(quantity):
    array = sorted([random.randint(-9999999, 99999999)
                    for _ in range(quantity)], reverse=True)
    return array


def generate_array_suit(quantity, best, worst, random):
    result = {}
    if random:
        random_array = generate_random_array(quantity)
        result[RANDOM] = random_array
    if best:
        best_array = generate_best_case_array(quantity)
        result[BEST] = best_array
    if worst:
        worst_array = generate_worst_case_array(quantity)
        result[WORST] = worst_array
    return result


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS]'.format(
            os.path.basename(
                sys.argv[0])),
        description='Generate arrays')
    parser.add_argument('-n', '--num', type=int, dest='num', default=1000,
                        help='number of elements to be generated')
    parser.add_argument('-b', '--best', action="store_true", dest='best',
                        help='generate best case array')
    parser.add_argument('-w', '--worst', action="store_true", dest='worst',
                        help='generate worst case array')
    parser.add_argument('-r', '--random', action="store_true", dest='random',
                        help='generate random case array')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        dest='output',
        help='choose, whether to print result on the screen, or write into file')
    args = parser.parse_args()

    result = generate_array_suit(args.num, args.best, args.worst, args.random)
    if args.output:
        write_json_in_file(args.output, result)
    else:
        pprint(result)


if __name__ == '__main__':
    sys.exit(main())
