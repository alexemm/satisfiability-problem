from resolution_calculus import load_json, decide_unsat

from cnf_formula import create_clause_set, CNFClauseSet

import os


def test_unsat():
    directory = "test/unsat"
    test_cases = [load_json('%s/%s' % (directory, file)) for file in os.listdir(directory)]
    for i, test_case in enumerate(test_cases):
        print("Test: %i" % (i + 1))
        assert test_case['unsat'] == decide_unsat(create_clause_set(test_case['clause_set']))
        print("Test successful")


def test_horn_sat():
    directory = "test/unsat"
    test_cases = [load_json('%s/%s' % (directory, file)) for file in os.listdir(directory)]
    for i, test_case in enumerate(test_cases):
        print("Test: %i" % (i + 1))
        print('formula: ' + CNFClauseSet(create_clause_set(test_case['clause_set'])).get_formula())
        print("Is Horn formula: " + str(CNFClauseSet(create_clause_set(test_case['clause_set'])).is_horn_formula()))


if __name__ == "__main__":
    test_unsat()
    test_horn_sat()
