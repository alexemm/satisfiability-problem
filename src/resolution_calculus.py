from typing import Set

import json


class Variable:

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

    def __init__(self, variable: Variable, postive: bool):
        self.variable = variable
        self.positive = postive

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.variable == other.variable and self.positive == other.positive

    def __hash__(self):
        return hash((self.variable, self.positive))

    def __str__(self):
        pre = ""
        if not self.positive:
            pre = "¬"
        return "%s%s" % (pre, str(self.variable))

    def __neg__(self):
        return Literal(self.variable, not self.positive)


class Clause:

    def __init__(self, literals: Set[Literal]):
        self.literals = literals

    def is_tautology(self) -> bool:
        literals = list(self.literals)
        for i in range(len(self.literals) - 1):
            for j in range(i + 1, len(self.literals)):
                if literals[i] == - literals[j]:
                    return True
        return False

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.literals == other.literals

    def __hash__(self):
        return hash(str(self.literals))

    def __str__(self):
        return '{' + ','.join([str(literal) for literal in self.literals]) + '}'

    def union(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Clause(self.literals.union(other.literals))

    def difference(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Clause(self.literals - other.literals)

    def __or__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.difference(other)


def create_literal(literal: str) -> Literal:
    positive = not literal.startswith('-')
    if not positive:
        literal = literal[1:]
    # import  pdb; pdb.set_trace()
    return Literal(Variable(literal), positive)


def create_clause_set(clauses) -> Set[Clause]:
    ret = set()
    for clause in clauses:
        ret.add(Clause(set(map(create_literal, clause))))
    return ret


def print_set(S):
    print([str(i) for i in S])


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
