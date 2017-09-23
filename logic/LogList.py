from copy import deepcopy


class LogList(list):
    """List, which can count the number of  permutations and comparison"""

    def __init__(self, array):
        new_copy = deepcopy(array)
        super().__init__(new_copy)
        self._permutation_count = 0

    def __setitem__(self, idx, value):
        self._permutation_count += 1
        super().__setitem__(idx, value)

    def permutations(self):
        return self._permutation_count // 2

    def swap(self, idx_one, idx_two):
        if idx_one == idx_two:
            self._permutation_count -= 2
        self[idx_one], self[idx_two] = self[idx_two], self[idx_one]
