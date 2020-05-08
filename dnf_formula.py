from typing import Set

from formula import Clause, Literal, ClauseSet


class DNFClause(Clause):
    """
    This class represents a Clause which is a set of literals in disjunctive Normal form.
    """

    def __init__(self, literals: Set[Literal]) -> None:
        super().__init__(literals)

    def is_unsat(self) -> bool:
        """
        Checks for any literal if the negative version is in it
        :return: bool whether this clause is unsatisfiable
        """
        return any([- literal in self.literals for literal in self.literals])

    def get_formula(self) -> str:
        """
        Returns string of formula which is a disjunction of literals
        :return: string of formula
        """
        return ' ∧ '.join([str(literal) for literal in self.literals])


class DNFClauseSet(ClauseSet):
    """
    Class which represents sets of clauses in DNF
    """

    def __init__(self, clause_set: Set[DNFClause]) -> None:
        super().__init__(clause_set)

    def get_formula(self) -> str:
        """
        Returns the String of formula which is represented by this set of clauses.
        :return: String of formula in DNF.
        """
        return ' ∨ '.join(["(%s)" % clause.get_formula() for clause in self.clause_set])
