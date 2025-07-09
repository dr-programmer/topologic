import numpy as np
from input_parser import parse_input
from parser import parse_expression, pretty_print, Var, Not, And, Or, Implies, Square, Diamond
from kripke_model import KripkeMatrix

def eval_ast(ast, kripke_matrix, var_map):
    """
    Recursively evaluate the AST using the KripkeMatrix and variable mapping.
    Returns a numpy array of results, one per world.
    """
    # Helper to add a temporary column to the KripkeMatrix for subexpression results
    def add_temp_column(matrix, col):
        # Add a new column to the matrix and return its index
        matrix = np.hstack([matrix, col.reshape(-1, 1)])
        return matrix, matrix.shape[1] - 1

    # We need to keep track of the current matrix and var_map as we add temp columns
    def _eval(ast, matrix, var_map):
        if isinstance(ast, Var):
            return matrix[:, var_map[ast.name]], matrix, var_map
        elif isinstance(ast, Not):
            res, matrix, var_map = _eval(ast.expr, matrix, var_map)
            # Add result as temp column
            matrix, idx_inner = add_temp_column(matrix, res)
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res_not = temp_km.i_not(idx_inner)
            matrix, idx = add_temp_column(matrix, res_not)
            return matrix[:, idx], matrix, {**var_map, f"_tmp{idx}": idx}
        elif isinstance(ast, And):
            left, matrix, var_map = _eval(ast.left, matrix, var_map)
            right, matrix, var_map = _eval(ast.right, matrix, var_map)
            matrix, idx_left = add_temp_column(matrix, left)
            matrix, idx_right = add_temp_column(matrix, right)
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res_and = temp_km.i_and(idx_left, idx_right)
            matrix, idx = add_temp_column(matrix, res_and)
            return matrix[:, idx], matrix, {**var_map, f"_tmp{idx}": idx}
        elif isinstance(ast, Or):
            left, matrix, var_map = _eval(ast.left, matrix, var_map)
            right, matrix, var_map = _eval(ast.right, matrix, var_map)
            matrix, idx_left = add_temp_column(matrix, left)
            matrix, idx_right = add_temp_column(matrix, right)
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res_or = temp_km.i_or(idx_left, idx_right)
            matrix, idx = add_temp_column(matrix, res_or)
            return matrix[:, idx], matrix, {**var_map, f"_tmp{idx}": idx}
        elif isinstance(ast, Implies):
            left, matrix, var_map = _eval(ast.left, matrix, var_map)
            right, matrix, var_map = _eval(ast.right, matrix, var_map)
            # Add left and right as temp columns to get their indices
            matrix, idx_left = add_temp_column(matrix, left)
            matrix, idx_right = add_temp_column(matrix, right)
            # Use a temporary KripkeMatrix with the extended matrix
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res = temp_km.i_implies(idx_left, idx_right)
            matrix, idx = add_temp_column(matrix, res)
            return matrix[:, idx], matrix, {**var_map, f"_tmp{idx}": idx}
        elif isinstance(ast, Square):
            inner, matrix, var_map = _eval(ast.expr, matrix, var_map)
            matrix, idx = add_temp_column(matrix, inner)
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res = temp_km.i_square(idx)
            matrix, idx2 = add_temp_column(matrix, res)
            return matrix[:, idx2], matrix, {**var_map, f"_tmp{idx2}": idx2}
        elif isinstance(ast, Diamond):
            inner, matrix, var_map = _eval(ast.expr, matrix, var_map)
            matrix, idx = add_temp_column(matrix, inner)
            temp_km = KripkeMatrix(
                {f"w{i}": {f"v{j}": matrix[i, j] for j in range(matrix.shape[1])} for i in range(matrix.shape[0])},
                kripke_matrix.access_matrix
            )
            res = temp_km.i_diamond(idx)
            matrix, idx2 = add_temp_column(matrix, res)
            return matrix[:, idx2], matrix, {**var_map, f"_tmp{idx2}": idx2}
        else:
            raise ValueError(f"Unknown AST node: {ast}")

    # Start with the original matrix and var_map
    res, _, _ = _eval(ast, kripke_matrix.matrix.copy(), var_map.copy())
    return res

def parse_and_evaluate_input(input_str):
    """
    Full pipeline: parse input, build KripkeMatrix, parse expr, evaluate AST.
    Returns a dict with all relevant data.
    """
    parsed = parse_input(input_str)
    # Build KripkeMatrix
    km = KripkeMatrix(
        {w: {v: parsed['matrix'][i][j] for j, v in enumerate(parsed['var_names'])} for i, w in enumerate(parsed['world_names'])},
        np.array(parsed['access_matrix'])
    )
    # Parse expression to AST
    ast = parse_expression(parsed['expr'])
    # Evaluate AST
    result = eval_ast(ast, km, parsed['var_map'])
    return {
        "ast": ast,
        "result": result,
        "kripke_matrix": km,
        "parsed": parsed
    }

if __name__ == "__main__":
    input_str = '''
worlds {
    w0: P=1, Q=0, R=1, S=0
    w1: P=0, Q=1, R=1, S=0
    w2: P=1, Q=1, R=0, S=0
}
access {
    w0: w0, w1, w2
    w1: w1, w2
    w2: w2
}
expr: #(P && @Q) -> !(R || S)
'''
    result = parse_and_evaluate_input(input_str)
    print("AST:")
    pretty_print(result["ast"])
    print("\nResult per world:\n", result["result"])
    print("\nKripke Matrix:")
    result["kripke_matrix"].print() 