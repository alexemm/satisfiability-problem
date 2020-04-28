from resolution_calculus import load_json, decide_unsat
from horn_sat import marker_algorithm
from cnf_formula import create_clause_set, CNFClauseSet, HornFormulaSet

import os

# TODO: Simplify code, so test cases are easier to read


def test_unsat():
    directory = "test/unsat"
    test_cases = [load_json('%s/%s' % (directory, file)) for file in os.listdir(directory)]
    for i, test_case in enumerate(test_cases):
        print("Test: %i" % (i + 1))
        print('formula: ' + CNFClauseSet(create_clause_set(test_case['clause_set'])).get_formula())
        print("Is Horn formula: " + str(CNFClauseSet(create_clause_set(test_case['clause_set'])).is_horn_formula()))
        assert test_case['unsat'] == decide_unsat(create_clause_set(test_case['clause_set']))
        print("Test successful")


def test_horn_sat():
    directory = "test/horn_sat"
    test_cases = [load_json('%s/%s' % (directory, file)) for file in os.listdir(directory)]
    for i, test_case in enumerate(test_cases):
        print("Test: %i" % (i + 1))
        print('formula: ' + HornFormulaSet(create_clause_set(test_case['clause_set'], horn=True)).get_horn_formula())
        result = marker_algorithm(HornFormulaSet(create_clause_set(test_case['clause_set'], horn=True)))
        assert test_case['horn_sat'] == (result is not None)
        if result is not None:
            print('Minimal Model: ' + str([str(literal) for literal in result]))


if __name__ == "__main__":
    test_unsat()
    test_horn_sat()
