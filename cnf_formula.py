from typing import Set, Iterable


# TODO: Refactor code for proper styling
# TODO: Add Abstract class for clause
# TODO: Add method for implemented algorithms inside classes (just import from the modules)
# TODO: change order of defined methods
# TODO: Check for right abstraction of classes (check in methods which have no type hint)

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


class CNFClause:
    """
    This class represents a Clause which is a set of literals. This
    """

    def __init__(self, literals: Set[Literal]):
        self.literals = literals

    def is_tautology(self) -> bool:
        """
        Returns, whether all fitting interpretations of this Clause are model of it
        :return: boolean, whether this formula is a tautology, or not
        """
        # TODO: Try to make use of any and list comp
        literals = list(self.literals)
        for i in range(len(self.literals) - 1):
            for j in range(i + 1, len(self.literals)):
                if literals[i] == - literals[j]:
                    return True
        return False

    def is_horn_clause(self) -> bool:
        """
        Returns, whether this Clause has maximum one positive literal, or not.
        :return: boolean, whether this clause is a Horn Clause
        """
        return sum([int(literal.positive) for literal in self.literals]) <= 1

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.literals == other.literals

    def __hash__(self):
        return hash(frozenset(self.literals))

    def __str__(self):
        return '{' + ','.join([str(literal) for literal in self.literals]) + '}'

    def union(self, other: 'CNFClause') -> 'CNFClause':
        """
        Returns the union of this clause and the other.
        :param other: Another clause
        :return: Clause, which is the union of both clauses
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return CNFClause(self.literals.union(other.literals))

    def difference(self, other) -> 'CNFClause':
        """
        Returns the difference between this clause and the other clause which was given. The result is the Clause with
        elements of the first clause without the elements of the second clause.
        :param other: Another clause
        :return: Returns the difference between both clauses A and B: A \\ B.
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return CNFClause(self.literals - other.literals)

    def __or__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.difference(other)

    def __len__(self):
        return len(self.literals)

    def right_side_given(self):
        """
        Is not implemented, because it refers to Horn clauses
        :return: None, but a NotImplemented is raised
        """
        raise NotImplemented

    def one_positive_many_negative(self):
        """
        Is not implemented, because it refers to Horn clauses
        :return: None, but a NotImplemented is raised
        """
        raise NotImplemented

    def just_negative(self):
        """
        Is not implemented, because it refers to Horn clauses
        :return: None, but a NotImplemented is raised
        """
        raise NotImplemented

    def get_positive_literals(self) -> Set[Literal]:
        """
        Returns a set of the literals which are only positive
        :return: set of positive literals
        """
        return set([literal for literal in self.literals if literal.positive])

    def get_negative_literals(self) -> Set[Literal]:
        """
        Returns a set of the literals which are only negative
        :return: set of negative literals
        """
        return set([literal for literal in self.literals if not literal.positive])

    def get_formula(self) -> str:
        """
        Returns string of formula which is a disjunction of literals
        :return: string of formula
        """
        return ' ∨ '.join([str(literal) for literal in self.literals])


class HornClause(CNFClause):
    """
    Class, which represents a subclass of CNFClauses which are Horn Clauses. Horn clauses consist of one positive
    literal at max.
    """

    def __init__(self, literals: Set[Literal]):
        super().__init__(literals)
        if not self.is_horn_clause():
            raise Exception

    def right_side_given(self) -> bool:
        """
        Evaluates, if this formula is in the form of (1 -> X)
        :return: boolean, whether clause is just one positive literal, or not
        """
        return len(self) == 1 and self.literals.copy().pop().positive

    def one_positive_many_negative(self) -> bool:
        """
        Evaluates, if this formula is in the form of ((X_1 and ... and X_k) -> X)
        :return: boolean, whether clause has many negative literals and one positive, or not
        """
        return len(self) != 1 and any([literal.positive for literal in self.literals])

    def just_negative(self) -> bool:
        """
        Evaluates, if this formula is in the form of ((X_1 and ... and X_k) -> 0)
        :return: boolean, whether clause just has many negative literals
        """
        return all([not literal.positive for literal in self.literals])

    def get_formula(self) -> str:
        """
        Returns string of formula which is in Horn writing (conjunction of negative literals (which are now positive)
        implicates positive literals)
        :return:
        """
        # Get right side
        right_side: str = "0"
        positive_literals: Set[Literal] = self.get_positive_literals()
        if len(positive_literals) == 1:
            right_side: str = "%s" % str(positive_literals.copy().pop().variable)
        # Get left side
        left_side: str = "1"
        negative_literals: Set[Literal] = self.get_negative_literals()
        if len(negative_literals) > 0:
            left_side: str = ' ∧ '.join([str(literal.variable) for literal in negative_literals])
        if len(negative_literals) > 1:
            left_side = "(%s)" % left_side
        # Assemble
        return "%s → %s" % (left_side, right_side)


class CNFClauseSet:
    """
    Class which represents sets of clauses in CNF
    """

    def __init__(self, clause_set: Set[CNFClause]):
        self.clause_set = clause_set

    def is_horn_formula(self) -> bool:
        """
        Returns whether this method is a formula which consists of Horn Clauses, or not
        :return: boolean, whether this clause set represents a Horn Formula
        """
        return all([clause.is_horn_clause() for clause in self.clause_set])

    def get_formula(self) -> str:
        """
        Returns the String of formula which is represented by this set of clauses.
        :return: String of formula in CNF.
        """
        return ' ∧ '.join(["(%s)" % clause.get_formula() for clause in self.clause_set])

    def __len__(self):
        return len(self.clause_set)

    def __str__(self):
        return '{' + ','. join((map(str, self.clause_set))) + '}'


class HornFormulaSet(CNFClauseSet):
    """
    Class which consists of clause set which represents Horn Formulas.
    """

    def __init__(self, clause_set: Set[HornClause]):
        super().__init__(clause_set)
        if not self.is_horn_formula():
            raise Exception

    def get_right_side_given(self):
        """
        Returns clauses in the form (1 -> X)
        :return: Horn Clauses of type 1 (1 -> X)
        """
        return set([clause for clause in self.clause_set if clause.right_side_given()])

    def get_one_positve_many_negative(self):
        """
        Returns clauses in the form of ((X_1 and ... and X_k) -> X)
        :return: Horn Clauses of type 2 ((X_1 and ... and X_k) -> X)
        """
        return set([clause for clause in self.clause_set if clause.one_positive_many_negative()])

    def get_just_negative(self):
        """
        Returns clauses in the form of ((X_1 and ... and X_k) -> 0)
        :return: Horn Clauses of type 3 ((X_1 and ... and X_k) -> 0)
        """
        return set([clause for clause in self.clause_set if clause.just_negative()])


def create_literal(literal: str) -> Literal:
    """
    Returns literal from given string
    :param literal: String of literal
    :return: Literal
    """
    positive = not literal.lstrip().startswith('-')
    if not positive:
        literal = literal[1:]
    return Literal(Variable(literal), positive)


def create_clause_set(clauses: Iterable[str], horn: bool = False) -> Set[CNFClause]:
    """
    Returns a clause set from given clauses (Optionally: Horn clauses)
    :param clauses:
    :param horn: Whether horn clauses should be returned or not
    :return: Set of clauses
    """
    # TODO: Maybe change return type to CNFClauseSet? (also change the doc then!)
    ret = set()
    for clause in clauses:
        if horn:
            ret.add(HornClause(set(map(create_literal, clause))))
        else:
            ret.add(CNFClause(set(map(create_literal, clause))))
    return ret


def print_set(S):
    """
    Prints clause sets
    :param S:
    :return:
    """
    # TODO: Reconsider, if needed after implementing string methods of classes
    print([str(i) for i in S])
