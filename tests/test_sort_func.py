#!/usr/bin/env python3
import unittest
import sys
import os
import random
import math

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

from logic.sort_functions import merge_sort, shell_sort, bubble_sort, hoare_sort, radix_sort
from logic.comparison_functions import less, greater


class BaseTestCases:
    class BaseTest(unittest.TestCase):
        sort_func = None

        def setUp(self):
            self.array_one = [101, -12, 99, 3, 2, 1]
            self.array_two = [random.random() for _ in range(100)]
            self.array_three = [random.random() for _ in range(500)]
            self.result_one = sorted(self.array_one)
            self.result_two = sorted(self.array_two)
            self.result_three = sorted(self.array_three)

        def tearDown(self):
            less.calls = 0
            greater.calls = 0

        def test_sort(self):
            result_one = self.sort_func(self.array_one)
            result_two = self.sort_func(self.array_two)
            result_three = self.sort_func(self.array_three)
            self.assertEqual(self.result_one, result_one)
            self.assertEqual(self.result_two, result_two)
            self.assertEqual(self.result_three, result_three)

        def test_reversed(self):
            result_one = self.sort_func(self.array_one, reverse=True)
            result_two = self.sort_func(self.array_two, reverse=True)
            result_three = self.sort_func(self.array_three, reverse=True)
            self.assertEqual(sorted(self.array_one, reverse=True), result_one)
            self.assertEqual(sorted(self.array_two, reverse=True), result_two)
            self.assertEqual(
                sorted(
                    self.array_three,
                    reverse=True),
                result_three)

        def test_key(self):
            cmp = less
            test_list = ["Hello", "my", "dear", "friend"]
            right_res = sorted(test_list, key=lambda x: len(x))
            my_res = self.sort_func(
                test_list, cmp=lambda x, y: cmp(
                    len(x), len(y)))
            self.assertEqual(right_res, my_res)

        def test_key_and_reverse(self):
            cmp = less
            test_list = ["Hello", "my", "dear", "friend"]
            right_res = sorted(test_list, key=lambda x: len(x), reverse=True)
            my_res = self.sort_func(
                test_list, cmp=lambda x, y: cmp(
                    len(x), len(y)), reverse=True)
            self.assertEqual(right_res, my_res)


class TestBubble(BaseTestCases.BaseTest):
    def setUp(self):
        self.sort_func = bubble_sort
        super().setUp()


class TestMerge(BaseTestCases.BaseTest):
    def setUp(self):
        self.sort_func = merge_sort
        super().setUp()


class TestHoare(BaseTestCases.BaseTest):
    def setUp(self):
        self.sort_func = hoare_sort
        super().setUp()


class TestShell(BaseTestCases.BaseTest):
    def setUp(self):
        self.sort_func = shell_sort
        super().setUp()

    def test_shell_step(self):
        marcin_ciur = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
        marcin_step = shell_sort(self.array_one, step=iter(marcin_ciur))
        step_one = shell_sort(self.array_one, step=iter([1]))
        hibbard_step = shell_sort(
            self.array_two, step=hibbard(
                0, len(
                    self.array_two)))
        tokuda_step = shell_sort(
            self.array_two, step=tokuda(
                0, len(
                    self.array_two)))
        self.assertEqual(self.result_one, marcin_step)
        self.assertEqual(self.result_one, step_one)
        self.assertEqual(self.result_two, hibbard_step)
        self.assertEqual(self.result_two, tokuda_step)


class TestRadix(unittest.TestCase):
    def setUp(self):
        self.array_one = [123, -12, 89, 23, 52, 61, -25, -10, 10]
        self.array_two = [random.randint(-999999, 9999999)
                          for _ in range(1000)]
        self.array_three = [
            random.randint(-999999, 9999999) for _ in range(5000)]
        self.result_one = sorted(self.array_one)
        self.result_two = sorted(self.array_two)
        self.result_three = sorted(self.array_three)

    def tearDown(self):
        less.calls = 0
        greater.calls = 0

    def test_radix(self):
        result_one = radix_sort(self.array_one)
        result_two = radix_sort(self.array_two)
        result_three = radix_sort(self.array_three)
        self.assertEqual(self.result_one, result_one)
        self.assertEqual(self.result_two, result_two)
        self.assertEqual(self.result_three, result_three)

    def test_radix_reverse(self):
        result_one = radix_sort(self.array_one, reverse=True)
        result_two = radix_sort(self.array_two, reverse=True)
        self.assertEqual(self.result_one[::-1], result_one)
        self.assertEqual(self.result_two[::-1], result_two)


def tokuda(i, stop):
    result = math.ceil((pow(9, i) - pow(4, i))
                       / (5 * pow(4, i - 1)))
    while result <= stop:
        i += 1
        yield result
        result = math.ceil((pow(9, i) - pow(4, i))
                           / (5 * pow(4, i - 1)))


def hibbard(i, stop):
    while pow(2, i) - 1 <= stop:
        i += 1
        yield pow(2, i) - 1


if __name__ == '__main__':
    unittest.main()
