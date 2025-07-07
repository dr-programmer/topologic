import numpy as np

from kripke_model import KripkeMatrix

valuation = {
    "w0": {"P": 0, "Q": 1, "R": 0},
    "w1": {"P": 1, "Q": 1, "R": 0},
    "w2": {"P": 1, "Q": 1, "R": 1},
}

access = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1]])

timeline = KripkeMatrix(valuation, access) 

timeline.print()

timeline.show_knowledge()

print(timeline.i_and(0, 2))
print(timeline.i_or(0, 2))
print(timeline.i_not(0))