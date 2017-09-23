#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.comparison_functions import less, greater


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.array = [1, 2, 3, 4, 5]

    def tearDown(self):
        less.calls = 0
        greater.calls = 0

    def test_less(self):
        for x in self.array:
            less(x, 1)
        self.assertEqual(5, less.calls)

    def test_less_again(self):
        for x in self.array:
            less(x, 1)
        self.assertEqual(5, less.calls)

    def test_greater(self):
        for x in self.array:
            greater(x, 1)
        self.assertEqual(5, greater.calls)

    def test_inner_greater(self):
        def key(x, y):
            return greater(x, y)
        for item in self.array:
            key(item, 1)
        self.assertEqual(5, greater.calls)

    def test_inner_less(self):
        def key(x, y):
            return less(x, y)
        for item in self.array:
            key(item, 1)
        self.assertEqual(5, less.calls)

    def test_inner_less_another_way(self):
        def key(x, y):
            return less(y, x)
        for item in self.array:
            key(item, 1)
        self.assertEqual(5, less.calls)

    def test_inner_greater_another_way(self):
        def key(x, y):
            return greater(y, x)
        for item in self.array:
            key(item, 1)
        self.assertEqual(5, greater.calls)


if __name__ == '__main__':
    unittest.main()
