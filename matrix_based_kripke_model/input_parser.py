import re

def parse_input(input_str):
    # Extract blocks
    worlds_block = re.search(r"worlds\s*{([^}]*)}", input_str, re.DOTALL)
    access_block = re.search(r"access\s*{([^}]*)}", input_str, re.DOTALL)
    expr_block = re.search(r"expr:\s*(.*)", input_str)

    if not (worlds_block and access_block and expr_block):
        raise ValueError("Input must contain 'worlds', 'access', and 'expr' sections.")

    # Parse worlds
    worlds = {}
    var_names = set()
    for line in worlds_block.group(1).strip().splitlines():
        if not line.strip():
            continue
        world, assigns = line.split(":")
        world = world.strip()
        assigns = assigns.strip()
        assigns = assigns.replace(",", " ")
        var_dict = {}
        for assign in assigns.split():
            if not assign:
                continue
            var, val = assign.split("=")
            var = var.strip()
            val = int(val.strip())
            var_dict[var] = val
            var_names.add(var)
        worlds[world] = var_dict

    # Sort variable names for consistent column order
    var_names = sorted(var_names)
    world_names = sorted(worlds.keys())

    # Build matrix for KripkeMatrix
    matrix = []
    for w in world_names:
        row = [worlds[w].get(var, 0) for var in var_names]
        matrix.append(row)

    # Parse access
    access = []
    access_dict = {}
    for line in access_block.group(1).strip().splitlines():
        if not line.strip():
            continue
        world, targets = line.split(":")
        world = world.strip()
        targets = [t.strip() for t in targets.split(",") if t.strip()]
        access_dict[world] = targets

    # Build access matrix
    access_matrix = []
    for w_from in world_names:
        row = []
        for w_to in world_names:
            row.append(1 if w_to in access_dict[w_from] else 0)
        access_matrix.append(row)

    # Extract expression
    expr = expr_block.group(1).strip()

    # Build variable name to index map
    var_map = {var: idx for idx, var in enumerate(var_names)}

    return {
        "world_names": world_names,
        "var_names": var_names,
        "matrix": matrix,
        "access_matrix": access_matrix,
        "expr": expr,
        "var_map": var_map
    }

# Example usage
if __name__ == "__main__":
    input_str = '''
worlds {
    w0: P=1, Q=0, R=1
    w1: P=0, Q=1, R=1
    w2: P=1, Q=1, R=0
}
access {
    w0: w0, w1, w2
    w1: w1, w2
    w2: w2
}
expr: #(P && @Q) -> !(R || S)
'''
    result = parse_input(input_str)
    from pprint import pprint
    pprint(result) 