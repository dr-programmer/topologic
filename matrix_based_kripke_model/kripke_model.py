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

    def i_and(self, *args) -> np.array:
        return reduce(lambda x, y: self.matrix[:,x] * self.matrix[:,y], args)
    
    def i_or(self, *args) -> np.array:
        return reduce(lambda x, y: np.maximum(self.matrix[:,x], self.matrix[:,y]), args)
    
    def i_not(self, var) -> np.array:
        return ((self.access_matrix @ self.matrix)[:,var] == 0).astype(int)
