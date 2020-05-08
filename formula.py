from typing import Set


class Variable:
    """
    Class which just represents a unique Variable with its name. Objects of it are hashable, and therefore usable in a
    set.
    """

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Literal:
    """
    This class represents a literal in e.g. a boolean formula in CNF. A literal is a Variable, which can be either
    positive or negative.
    """

    def __init__(self, variable: Variable, postive: bool):
        self.variable = variable
        self.positive = postive

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.variable == other.variable and self.positive == other.positive

    def __hash__(self):
        return hash(str(self.variable) + str(self.positive))

    def __str__(self):
        pre = ""
        if not self.positive:
            pre = "¬"
        return "%s%s" % (pre, str(self.variable))

    def __neg__(self):
        return Literal(self.variable, not self.positive)


class Clause:
    """
    Abstract class Clause which is a set of literals
    """

    def __init__(self, literals: Set[Literal]):
        self.literals = literals

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.literals == other.literals

    def __hash__(self):
        return hash(frozenset(self.literals))

    def __str__(self):
        return '{' + ','.join([str(literal) for literal in self.literals]) + '}'

    def __len__(self):
        return len(self.literals)


class ClauseSet:
    """
    Class which represents sets of clauses
    """

    def __init__(self, clause_set: Set[Clause]):
        self.clause_set = clause_set

    def __len__(self):
        return len(self.clause_set)

    def __str__(self):
        return '{' + ','.join((map(str, self.clause_set))) + '}'
