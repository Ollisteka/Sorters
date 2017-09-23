#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.LogList import LogList


class MyTestCase(unittest.TestCase):
    def setUp(self):
        a = [1, 2, 3]
        b = ["Hi", "Python", "!"]
        c = [[1, 2, 3], [1, 2], [1]]
        self.list_int = LogList(a)
        self.list_string = LogList(b)
        self.list_list = LogList(c)

    def test_permutation_count(self):
        for name in ["list_int", "list_string", "list_list"]:
            #__getattr__и __getattr(self,name) узнать разницу
            array = self.__getattribute__(name)
            for i in range(len(array)):
                for j in range(len(array)):
                    array.swap(i, j)
            self.assertEqual(6, array.permutations())


if __name__ == '__main__':
    unittest.main()
