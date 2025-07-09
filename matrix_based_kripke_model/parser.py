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

# Example usage:
if __name__ == "__main__":
    expr_str = "#(P && @Q) -> !(R || S)"
    ast = parse_expression(expr_str)
    print("AST repr:", ast)
    print("\nPretty print:")
    pretty_print(ast) 