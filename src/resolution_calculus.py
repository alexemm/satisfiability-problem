from typing import Set

from cnf_formula import Clause

import json


def Res(K: Set[Clause]) -> Set[Clause]:
    K_list = list(K)
    res = set()
    for i in range(len(K_list) - 1):
        for j in range(i + 1, len(K_list)):
            for literal in list(K_list[i].literals):
                if - literal in K_list[j].literals:
                    resolute = (K_list[i] | K_list[j]) - Clause({literal, -literal})
                    if not resolute.is_tautology():
                        res.add(resolute)
                    break
    return K | res


def decide_unsat(K: Set[Clause]) -> bool:
    R: set[Clause] = set()
    S: set[Clause] = K
    while R != S:
        R = S
        S = Res(R)
        if Clause(set()) in S:
            return True
    return False


def load_json(file: str):
    with open(file) as f:
        ret = json.load(f)
    return ret
