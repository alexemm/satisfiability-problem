from itertools import product
from functools import reduce

class Formula:

    def __init__(self, formula: str):
        self.formula = formula

    def eval(self):
        return eval(self.formula)


formula = lambda A, B, C, D, V, W: reduce(lambda x, y: x * y, [
    A * D <= W,
    A * C <= B,
    V <= C,
    A * W <= V,
    B <= 0,
    A * D <= 0
])

possible_options = product(*[[0, 1] for _ in range(0, 6)])
solutions = [option for option in possible_options if formula(*option)]
print(solutions)