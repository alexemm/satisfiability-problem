from typing import Set

from cnf_formula import CNFClause

import json


def Res(K: Set[CNFClause]) -> Set[CNFClause]:
    """
    Resolution function which returns the resolutes of a given set of clauses.
    :param K: Set of clauses in CNF
    :return: All the resolutes united with K
    """
    K_list = list(K)
    res = set()
    for i in range(len(K_list) - 1):
        for j in range(i + 1, len(K_list)):
            for literal in list(K_list[i].literals):
                if - literal in K_list[j].literals:
                    resolute = (K_list[i] | K_list[j]) - CNFClause({literal, -literal})
                    if not resolute.is_tautology():
                        res.add(resolute)
                        break
    return K | res


def decide_unsat(K: Set[CNFClause]) -> bool:
    """
    Returns if given set of clauses is in CNF, or not
    :param K: Set of Clauses in CNF
    :return: bool, whether this formula is undecidable or not
    """
    R: set[CNFClause] = set()
    S: set[CNFClause] = K
    while R != S:
        R = S
        S = Res(R)
        if CNFClause(set()) in S:
            return True
    return False


def load_json(file: str):
    """
    Loads json file and returns list of list
    :param file: Path to file to load
    :return: List of lists from loaded JSON
    """
    # TODO: Put it into cnf_formula.py
    with open(file) as f:
        ret = json.load(f)
    return ret
