from cnf_formula import HornFormulaSet

# TODO: Change the set of literals into set of variables (literals are not needed in return), also add return type


def marker_algorithm(psi: HornFormulaSet):
    """
    Applies Marker Algorithm to given Horn Formula and returns either minimal model (if satisfiable) or None
    :param psi: Horn Formula represented as HornFormulaSet
    :return: Minimal model as set of Variables or None
    """
    N = set()
    M = set([X.literals.copy().pop() for X in psi.get_right_side_given()])
    while N != M:
        N = M
        M = M | set(
            [X.get_positive_literals().copy().pop() for X in psi.get_one_positve_many_negative() if
             set(map(lambda x: -x, X.get_negative_literals())) <= M])
        if any([set(map(lambda x: -x, clause.get_negative_literals())) <= M for clause in psi.get_just_negative()]):
            return None
    return M
