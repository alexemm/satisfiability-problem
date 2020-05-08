from itertools import product
from functools import reduce


class Formula:

    def __init__(self, formula: str):
        self.formula = formula

    def eval(self):
        return eval(self.formula)


formula = lambda A, B, C, D, E: reduce(lambda x, y: x * y, [
    max(A, 1 - D),
    1 - E,
    max(D, B),
    max(1 - D, E, B),
    max(1 - A, 1 - B),
    C,
    max(1 - A, 1 - B),
    max(1 - A, 1 - B)
])

possible_options = product(*[[0, 1] for _ in range(0, 5)])
solutions = [option for option in possible_options if formula(*option)]
print(solutions)