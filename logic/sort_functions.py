#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.comparison_functions import less, greater
from logic.LogList import LogList


def bubble_sort(iterable, cmp=None, reverse=False):
    """
    Return a new sorted list from the items in iterable, using bubble sort
    :param iterable:
    :param cmp:
    :param reverse:
    :return:
    """
    array = LogList(iterable)

    if reverse and cmp is None:
        def key(x, y):
            return less(x, y)
    elif not reverse and cmp is None:
        def key(x, y):
            return greater(x, y)
    elif reverse and cmp:
        def key(x, y):
            return cmp(x, y)
    elif not reverse and cmp:
        def key(x, y):
            return cmp(y, x)

    for _ in range(len(array)):
        for j in range(len(array) - 1):
            if key(array[j], array[j + 1]):
                array.swap(j + 1, j)
    return array


def __merge(array, temp_array, start, middle, end, key):
    """

    :type array: LogList
    :param temp_array:
    :param start:
    :param middle:
    :param end:
    :param key:
    :return:
    """
    left_edge = start
    right_edge = middle + 1
    length = end - start + 1
    for i in range(length):
        if right_edge > end or (
            left_edge <= middle and key(
                array[left_edge],
                array[right_edge])):
            temp_array[i] = array[left_edge]
            left_edge += 1
        else:
            temp_array[i] = array[right_edge]
            right_edge += 1
    for i in range(length):
        array[i + start] = temp_array[i]
    return array


def __merge_sort(array, temp_array, start, end, key):
    """

    :type array: LogList
    :param temp_array:
    :param start:
    :param end:
    :param key:
    :return:
    """
    if start == end:
        return
    middle = (start + end) // 2
    __merge_sort(array, temp_array, start, middle, key)
    __merge_sort(array, temp_array, middle + 1, end, key)
    array = __merge(array, temp_array, start, middle, end, key)
    return array


def merge_sort(iterable, cmp=None, reverse=False):
    """
    Return a new sorted list from the items in iterable, using merge sort
    :param iterable:
    :param cmp:
    :param reverse:
    :return:
    """
    array = LogList(iterable)
    if reverse and cmp is None:
        def key(x, y):
            return greater(x, y)
    elif not reverse and cmp is None:
        def key(x, y):
            return less(x, y)
    elif reverse and cmp:
        def key(x, y):
            return cmp(y, x)
    elif not reverse and cmp:
        def key(x, y):
            return cmp(x, y)
    temp_array = [0] * len(array)
    end = len(array) - 1
    array = __merge_sort(array, temp_array, 0, end, key)
    return array


def __generate_default_step(start, stop):
    while start > stop:
        start //= 2
        yield start


def shell_sort(iterable, step=None, cmp=None, reverse=False):
    """
    Return a new sorted list from the items in iterable, using Shell sort.
    :param iterable:
    :param step:
    :param cmp:
    :param reverse:
    :return:
    """
    array = LogList(iterable)
    if step is None:
        step = __generate_default_step(len(array), 0)
        step_len = next(step)
    else:
        step_len = next(step)
    if reverse and cmp is None:
        def key(x, y):
            return less(x, y)
    elif not reverse and cmp is None:
        def key(x, y):
            return greater(x, y)
    elif reverse and cmp:
        def key(x, y):
            return cmp(x, y)
    elif not reverse and cmp:
        def key(x, y):
            return cmp(y, x)
    while True:
        for i in range(len(array) - step_len):
            j = i
            while j >= 0 and key(array[j], array[j + step_len]):
                array.swap(j + step_len, j)
                j -= step_len
        try:
            step_len = next(step)
        except StopIteration:
            break
    return array


def __partition(array, start, end, cmp, reverse):
    if reverse and cmp is None:
        def key(x, y):
            return greater(x, y)
    elif not reverse and cmp is None:
        def key(x, y):
            return less(x, y)
    elif reverse and cmp:
        def key(x, y):
            return cmp(y, x)
    elif not reverse and cmp:
        def key(x, y):
            return cmp(x, y)
    # pivot_index = random.randint(start, end)
    pivot_index = (start + end + 1) // 2
    # pivot_index = end
    pivot = array[pivot_index]
    left_index = start
    right_index = end
    while left_index < right_index:
        while key(array[left_index], pivot):
            left_index += 1
        while not key(
                array[right_index],
                pivot) and array[right_index] != pivot:
            right_index -= 1
        if left_index < right_index:
            array.swap(left_index, right_index)
    return left_index


def __hoare_sort(array, start, end, key, reverse):
    if end - start < 1:
        return
    pivot_index = __partition(array, start, end, key, reverse)
    __hoare_sort(array, start, pivot_index - 1, key, reverse)
    __hoare_sort(array, pivot_index, end, key, reverse)


def hoare_sort(iterable, cmp=None, reverse=False):
    """
    Return a new sorted list from the items in iterable, using quick (Hoare) sort.
    :param iterable:
    :param cmp:
    :param reverse:
    :return:
    """
    array = LogList(iterable)
    __hoare_sort(array, 0, len(array) - 1, cmp, reverse)
    return array


def radix_sort(iterable, reverse=False, radix=10):
    """
    Return a new sorted list from the integers in iterable, using radix sort.
    Integers can be both positive and negative.
    :param iterable:
    :param reverse:
    :param radix:
    :return:
    """
    const = radix * 2 - 1

    if reverse:
        shift = dict(zip(range(const), range(const - 1, -1, -1)))
    else:
        shift = dict(zip(range(const), range(const)))

    offset = radix - 1

    array = LogList(iterable)
    for x in range(radix + 1):
        buckets = [LogList([]) for _ in range(radix + offset)]
        for number in array:
            num = int((number / radix ** x) % radix)
            if not less(number, 0):
                buckets[shift[num + offset]].append(number)
            else:
                buckets[shift[num]].append(number)
        array = LogList([])
        for section in [bucket for bucket in buckets if bucket]:
            array.extend(section)
        if len([bucket for bucket in buckets if bucket]) == 1:
            break
    return array
