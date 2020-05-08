from typing import Set, Optional

from propositional_calculus.cnf_formula import HornFormulaSet, Variable


def marker_algorithm(psi: HornFormulaSet) -> Optional[Set[Variable]]:
    """
    Applies Marker Algorithm to given Horn Formula and returns either minimal model (if satisfiable) or None
    :param psi: Horn Formula represented as HornFormulaSet
    :return: Minimal model as set of Variables or None
    """
    N: Set[Variable] = set()
    M: Set[Variable] = set([X.literals.copy().pop().variable for X in psi.get_right_side_given()])
    while N != M:
        N: Set[Variable] = M
        M: Set[Variable] = M | set(
            [X.get_positive_literals().copy().pop().variable for X in psi.get_one_positve_many_negative() if
             set([x.variable for x in X.get_negative_literals()]) <= M])
        if any([set([x.variable for x in clause.get_negative_literals()]) <= M for clause in psi.get_just_negative()]):
            return None
    return M
