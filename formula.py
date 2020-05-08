from typing import Set


class Variable:
    """
    Class which just represents a unique Variable with its name. Objects of it are hashable, and therefore usable in a
    set.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name

    def __eq__(self, other: 'Variable') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name


class Literal:
    """
    This class represents a literal in e.g. a boolean formula in CNF. A literal is a Variable, which can be either
    positive or negative.
    """

    def __init__(self, variable: Variable, postive: bool) -> None:
        self.variable: Variable = variable
        self.positive: bool = postive

    def __eq__(self, other: 'Literal') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.variable == other.variable and self.positive == other.positive

    def __hash__(self) -> int:
        return hash(str(self.variable) + str(self.positive))

    def __str__(self) -> str:
        pre: str = ""
        if not self.positive:
            pre: str = "¬"
        return "%s%s" % (pre, str(self.variable))

    def __neg__(self) -> 'Literal':
        return Literal(self.variable, not self.positive)


class Clause:
    """
    Abstract class Clause which is a set of literals
    """

    def __init__(self, literals: Set[Literal]) -> None:
        self.literals: Set[Literal] = literals

    def __eq__(self, other: 'Clause') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.literals == other.literals

    def __hash__(self) -> int:
        return hash(frozenset(self.literals))

    def __str__(self) -> str:
        return '{' + ','.join([str(literal) for literal in self.literals]) + '}'

    def __len__(self) -> int:
        return len(self.literals)


class ClauseSet:
    """
    Class which represents sets of clauses
    """

    def __init__(self, clause_set: Set[Clause]) -> None:
        self.clause_set: Set[Clause] = clause_set

    def __len__(self) -> int:
        return len(self.clause_set)

    def __str__(self) -> str:
        return '{' + ','.join((map(str, self.clause_set))) + '}'
