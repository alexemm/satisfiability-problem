from typing import Set


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

    def is_horn_clause(self):
        return sum([int(literal.positive) for literal in self.literals]) <= 1

    def get_horn_clause(self):
        if self.is_horn_clause():
            return HornClause(self.literals)

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

    def __len__(self):
        return len(self.literals)

    def right_side_given(self):
        raise NotImplemented

    def one_positive_many_negative(self):
        raise NotImplemented

    def just_negative(self):
        raise NotImplemented

    def get_positive_literals(self):
        return set([literal for literal in self.literals if literal.positive])

    def get_negative_literals(self):
        return set([literal for literal in self.literals if not literal.positive])


class HornClause(Clause):

    def __init__(self, literals: Set[Literal]):
        super().__init__(literals)
        if not self.is_horn_clause():
            raise Exception

    def right_side_given(self):
        """
        Evaluates, if this formula is in the form of (1 -> X)
        :return:
        """
        return len(self) == 1 and self.literals.copy().pop().positive

    def one_positive_many_negative(self):
        """
        Evaluates, if this formula is in the form of ((X_1 and ... and X_k) -> X)
        :return:
        """
        return len(self) != 1 and any([literal.positive for literal in self.literals])

    def just_negative(self):
        """
        Evaluates, if this formula is in the form of ((X_1 and ... and X_k) -> 0)
        :return:
        """
        return all([not literal.positive for literal in self.literals])


class CNFClauseSet:

    def __init__(self, clause_set: Set[Clause]):
        self.clause_set = clause_set

    def is_horn_formula(self):
        return all([clause.is_horn_clause() for clause in self.clause_set])

    def get_formula(self):
        return ' ∧ '.join(
            [str(clause).replace('{', '(').replace('}', ')').replace(',', ' ∨ ') for clause in self.clause_set])


class HornFormulaSet(CNFClauseSet):

    def __init__(self, clause_set: Set[HornClause]):
        super().__init__(clause_set)
        if not self.is_horn_formula():
            raise Exception

    def get_right_side_given(self):
        """
        Returns clauses in the form (1 -> X)
        :return:
        """
        return set([clause for clause in self.clause_set if clause.right_side_given()])

    def get_one_positve_many_negative(self):
        """
        Returns clauses in the form of ((X_1 and ... and X_k) -> X)
        :return:
        """
        return set([clause for clause in self.clause_set if clause.one_positive_many_negative()])

    def get_just_negative(self):
        """
        Returns clauses in the form of ((X_1 and ... and X_k) -> 0)
        :return:
        """
        return set([clause for clause in self.clause_set if clause.just_negative()])

    def get_horn_formula(self):
        type1 = " ∧ ".join(['(1 -> %s)' % clause.literals.copy().pop() for clause in self.get_right_side_given()])
        type2 = " ∧ ".join(['((%s)-> %s)' % (
            " ∧ ".join(map(lambda x: str(-x), clause.get_negative_literals())),
            str(clause.get_positive_literals().copy().pop())) for
                            clause in self.get_one_positve_many_negative()])
        type3 = " ∧ ".join(
            ['((%s) -> 0)' % " ∧ ".join(map(lambda x: str(-x), clause.get_negative_literals())) for clause in
             self.get_just_negative()])
        return ' ∧ '.join([i for i in [type1, type2, type3]])


def create_literal(literal: str) -> Literal:
    positive = not literal.startswith('-')
    if not positive:
        literal = literal[1:]
    return Literal(Variable(literal), positive)


def create_clause_set(clauses, horn=False) -> Set[Clause]:
    ret = set()
    for clause in clauses:
        if horn:
            ret.add(HornClause(set(map(create_literal, clause))))
        else:
            ret.add(Clause(set(map(create_literal, clause))))
    return ret


def print_set(S):
    print([str(i) for i in S])
