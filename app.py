from typing import Set, Optional

from flask import Flask, request, jsonify
from flask.wrappers import Response

from propositional_calculus.cnf_formula import HornClause, create_clause_set, HornFormulaSet
from propositional_calculus.formula import Variable
from propositional_calculus.horn_sat import marker_algorithm


app: Flask = Flask(__name__)


@app.route("/horn-sat", methods=["POST"])
def horn_sat() -> Response:
    formula: HornFormulaSet = HornFormulaSet(create_clause_set(request.form['formula'], horn=True))
    result: Optional[Set[Variable]] = marker_algorithm(formula)
    return_dict = {
        "minimal": result,
        "unsat": result is not None
    }
    return jsonify(return_dict)


if __name__ == "__main__":
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
