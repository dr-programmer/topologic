import numpy as np
from typing import Dict
from typing import Tuple
import pandas as pd
from functools import reduce

class KripkeMatrix:
    def __init__(self, worlds: Dict, access_matrix: np.array) -> None:
        self.matrix = np.array([[value for value in world.values()] for world in worlds.values()])
        self.access_matrix = access_matrix

    def _print(self, matrix, row_labels, column_labels):
        print(pd.DataFrame(matrix, index=row_labels, columns=column_labels))

    def _generate_labels(self, row_name, column_name, rows, columns) -> Tuple:
        row_labels = [row_name + str(i) for i in range(rows)]
        column_labels = [column_name + str(i) for i in range(columns)]
        return (row_labels, column_labels)

    def print(self):
        world_labels, value_labels = self._generate_labels("World-", "P-", *self.matrix.shape)
        self._print(self.matrix, world_labels, value_labels)

    def show_knowledge(self, do_print: bool = True) -> np.array:
        visibility = self.access_matrix @ self.matrix
        rows, columns = self._generate_labels("Times from World-", "Sees P-", *visibility.shape)
        if(do_print): self._print(visibility, rows, columns)
        return visibility

    def _and(self, *args) -> np.array:
        return reduce(lambda x, y: x * y, args)

    def i_and(self, *args) -> np.array:
        return self._and(*[self.matrix[:, x] for x in args])

    def _or(self, *args) -> np.array:
        return reduce(lambda x, y: np.maximum(x, y), args)

    def i_or(self, *args) -> np.array:
        return self._or(*[self.matrix[:, x] for x in args])

    def _not(self, arr) -> np.array:
        return (arr == 0).astype(int)

    def i_not(self, var) -> np.array:
        return self._not((self.access_matrix @ self.matrix)[:, var])

    def i_implies(self, cond, res) -> np.array:
        # Compute (not cond) or res for each world
        neg_cond = self._not(self.matrix[:, cond])
        res_col = self.matrix[:, res]
        implication = self._or(neg_cond, res_col)
        # Aggregate what each world sees via accessibility
        seen = self.access_matrix @ implication
        # For each world, implication holds if all accessible worlds see True (1)
        row_sums = self.access_matrix.sum(axis=1)
        # If a world sees no worlds, treat as vacuously true
        vacuously_true = (row_sums == 0)
        holds = (seen == row_sums)
        return np.where(vacuously_true, 1, holds.astype(int))

    def i_square(self, var) -> np.array:
        # □p: true in w iff p holds in all accessible worlds from w
        prop_col = self.matrix[:, var]
        # For each world, get the minimum (AND) over accessible worlds
        seen = self.access_matrix @ prop_col
        row_sums = self.access_matrix.sum(axis=1)
        # If a world sees no worlds, □p is vacuously true
        vacuously_true = (row_sums == 0)
        holds = (seen == row_sums)
        return np.where(vacuously_true, 1, holds.astype(int))

    def i_diamond(self, var) -> np.array:
        # ◇p: true in w iff p holds in at least one accessible world from w
        prop_col = self.matrix[:, var]
        # For each world, get the sum (OR) over accessible worlds
        seen = self.access_matrix @ prop_col
        # If a world sees no worlds, ◇p is vacuously false
        row_sums = self.access_matrix.sum(axis=1)
        vacuously_false = (row_sums == 0)
        holds = (seen > 0)
        return np.where(vacuously_false, 0, holds.astype(int))
