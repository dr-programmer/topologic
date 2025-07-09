import re

# AST Node definitions
class Expr:
    pass

class Var(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

class Not(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Not({self.expr})"

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"And({self.left}, {self.right})"

class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Or({self.left}, {self.right})"

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Implies({self.left}, {self.right})"

class Square(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Square({self.expr})"

class Diamond(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Diamond({self.expr})"

# Tokenizer
TOKEN_REGEX = re.compile(r"\s*(->|&&|\|\||!|#|@|\(|\)|[A-Za-z_][A-Za-z0-9_]*)")

def tokenize(s):
    tokens = TOKEN_REGEX.findall(s)
    return [t for t in tokens if t.strip()]

# Recursive descent parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        tok = self.peek()
        if expected and tok != expected:
            raise SyntaxError(f"Expected '{expected}', got '{tok}'")
        self.pos += 1
        return tok

    def parse(self):
        return self.parse_implies()

    def parse_implies(self):
        left = self.parse_or()
        while self.peek() == "->":
            self.consume("->")
            right = self.parse_implies()
            left = Implies(left, right)
        return left

    def parse_or(self):
        left = self.parse_and()
        while self.peek() == "||":
            self.consume("||")
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self):
        left = self.parse_unary()
        while self.peek() == "&&":
            self.consume("&&")
            right = self.parse_unary()
            left = And(left, right)
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok == "!":
            self.consume("!")
            return Not(self.parse_unary())
        elif tok == "#":
            self.consume("#")
            return Square(self.parse_unary())
        elif tok == "@":
            self.consume("@")
            return Diamond(self.parse_unary())
        elif tok == "(":
            self.consume("(")
            expr = self.parse_implies()
            self.consume(")")
            return expr
        else:
            return Var(self.consume())

def parse_expression(s):
    tokens = tokenize(s)
    parser = Parser(tokens)
    expr = parser.parse()
    if parser.peek() is not None:
        raise SyntaxError(f"Unexpected token: {parser.peek()}")
    return expr

def pretty_print(expr, indent=0):
    prefix = "  " * indent
    if isinstance(expr, Var):
        print(f"{prefix}Var({expr.name})")
    elif isinstance(expr, Not):
        print(f"{prefix}Not")
        pretty_print(expr.expr, indent + 1)
    elif isinstance(expr, And):
        print(f"{prefix}And")
        pretty_print(expr.left, indent + 1)
        pretty_print(expr.right, indent + 1)
    elif isinstance(expr, Or):
        print(f"{prefix}Or")
        pretty_print(expr.left, indent + 1)
        pretty_print(expr.right, indent + 1)
    elif isinstance(expr, Implies):
        print(f"{prefix}Implies")
        pretty_print(expr.left, indent + 1)
        pretty_print(expr.right, indent + 1)
    elif isinstance(expr, Square):
        print(f"{prefix}Square")
        pretty_print(expr.expr, indent + 1)
    elif isinstance(expr, Diamond):
        print(f"{prefix}Diamond")
        pretty_print(expr.expr, indent + 1)
    else:
        print(f"{prefix}Unknown({expr})")

import numpy as np

def parse_kripke_input(input_str):
    # Extract blocks
    worlds_block = re.search(r"worlds\s*{([^}]*)}", input_str, re.DOTALL)
    access_block = re.search(r"access\s*{([^}]*)}", input_str, re.DOTALL)
    expr_block = re.search(r"expr\s*:\s*(.*)", input_str)

    if not (worlds_block and access_block and expr_block):
        raise ValueError("Input must contain 'worlds { ... }', 'access { ... }', and 'expr: ...' sections.")

    # Parse worlds
    worlds_lines = [line.strip() for line in worlds_block.group(1).strip().splitlines() if line.strip()]
    valuation = {}
    var_names = set()
    world_names = []
    for line in worlds_lines:
        world, rest = line.split(":", 1)
        world = world.strip()
        world_names.append(world)
        assignments = rest.split(",")
        valuation[world] = {}
        for assign in assignments:
            if assign.strip():
                var, val = assign.strip().split("=")
                var = var.strip()
                val = int(val.strip())
                valuation[world][var] = val
                var_names.add(var)

    var_names = sorted(var_names)
    world_names = sorted(world_names)

    # Ensure all worlds have all variables (default to 0)
    for world in valuation:
        for var in var_names:
            if var not in valuation[world]:
                valuation[world][var] = 0

    # Parse access
    access_lines = [line.strip() for line in access_block.group(1).strip().splitlines() if line.strip()]
    access_dict = {}
    for line in access_lines:
        world, rest = line.split(":", 1)
        world = world.strip()
        accessible = [w.strip() for w in rest.split(",") if w.strip()]
        access_dict[world] = accessible

    # Build access matrix
    n = len(world_names)
    access_matrix = np.zeros((n, n), dtype=int)
    world_idx = {w: i for i, w in enumerate(world_names)}
    for w_from, w_tos in access_dict.items():
        i = world_idx[w_from]
        for w_to in w_tos:
            j = world_idx[w_to]
            access_matrix[i, j] = 1

    # Build valuation in the format KripkeMatrix expects (ordered dict of worlds)
    ordered_valuation = {w: {v: valuation[w][v] for v in var_names} for w in world_names}

    # Parse expr
    expr_str = expr_block.group(1).strip()
    expr_ast = parse_expression(expr_str)

    return {
        "valuation": ordered_valuation,
        "access_matrix": access_matrix,
        "expr_ast": expr_ast,
        "var_names": var_names,
        "world_names": world_names,
    }

# Example usage:
if __name__ == "__main__":
    expr_str = "#(P && @Q) -> !(R || S)"
    ast = parse_expression(expr_str)
    print("AST repr:", ast)
    print("\nPretty print:")
    pretty_print(ast) 