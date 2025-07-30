# Topologic: Matrix-Based Intuitionistic Logic Evaluator

## Overview

Topologic is a Python-based implementation of a **matrix-based intuitionistic logic evaluator** that uses Kripke models to evaluate intuitionistic logic expressions. This project provides a powerful tool for constructive mathematics, formal verification, type theory, and reasoning about information growth and constructive proofs.

## What is Intuitionistic Logic?

Intuitionistic logic (also called constructive logic) is a non-classical logic that rejects the law of excluded middle and double negation elimination. Unlike classical logic, intuitionistic logic is based on constructive reasoning where:

- **Truth requires evidence**: A proposition is only considered true if there's a constructive proof
- **Implication is constructive**: `p → q` means "given a proof of p, we can construct a proof of q"
- **Negation is constructive**: `¬p` means "assuming p leads to a contradiction"
- **No law of excluded middle**: `p ∨ ¬p` is not universally valid

## What is a Kripke Model for Intuitionistic Logic?

A Kripke model for intuitionistic logic consists of:
- **Worlds**: Representing states of knowledge or information
- **Accessibility relations**: A partial order (reflexive and transitive) representing information growth
- **Valuations**: Monotonic assignments of truth values (once true, always true in accessible worlds)

This implementation uses matrix operations to efficiently compute intuitionistic logic expressions, making it suitable for both educational purposes and practical applications in constructive mathematics and type theory.

## Features

- **Intuitionistic Logic Support**: Full support for constructive implication and negation
- **Propositional Logic**: Support for AND (&&), OR (||), NOT (!), and IMPLIES (->)
- **Modal Operators**: Support for □ (necessity) and ◇ (possibility) in intuitionistic context
- **Matrix-Based Computation**: Efficient evaluation using NumPy matrix operations
- **Flexible Input Format**: Simple text-based input format for defining Kripke models
- **CLI Interface**: Command-line tool for easy evaluation of logic expressions
- **Visual Output**: Pretty-printed AST and matrix representations

## Project Structure

```
topologic/
├── matrix_based_kripke_model/     # Main implementation
│   ├── cli.py                     # Command-line interface
│   ├── kripke_model.py            # Core Kripke model implementation
│   ├── logic_eval.py              # Logic expression evaluator
│   ├── parser.py                  # Expression parser and AST
│   ├── input_parser.py            # Input file parser
│   ├── experiment.py              # Example experiments
│   ├── timeline.py                # Timeline/branching support
│   └── test_cases/                # Example test cases
│       ├── test_1.ikm
│       └── test_2.ikm
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd topologic
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- **numpy** (2.2.6): For efficient matrix operations
- **pandas** (2.3.0): For pretty-printing matrices
- **anytree** (2.13.0): For tree-based data structures
- **tabulate** (0.9.0): For formatted table output

## Usage

### Command Line Interface

The main way to use Topologic is through the command-line interface:

```bash
python matrix_based_kripke_model/cli.py <input_file>
```

### Input File Format

Input files use a simple `.ikm` (Interactive Kripke Model) format with three main sections:

1. **worlds**: Defines the worlds and their propositional variable assignments
2. **access**: Defines the accessibility relations between worlds
3. **expr**: The modal logic expression to evaluate

#### Example Input File

```ikm
worlds {
    w0: P=1, Q=0, R=1, S=0
    w1: P=0, Q=1, R=1, S=0
    w2: P=1, Q=1, R=0, S=0, Z=1
}
access {
    w0: w0, w1, w2
    w1: w1, w2
    w2: w2
}
expr: !R -> Z
```

### Syntax

#### Propositional Variables
- Use uppercase letters (P, Q, R, etc.) for propositional variables
- Assign values using `Variable=Value` where Value is 0 (false) or 1 (true)

#### Logic Operators
- **AND**: `&&` (conjunction)
- **OR**: `||` (disjunction)
- **NOT**: `!` (negation)
- **IMPLIES**: `->` (implication)

#### Modal Operators
- **Necessity**: `#` (□, "necessarily" - true in all accessible worlds)
- **Possibility**: `@` (◇, "possibly" - true in at least one accessible world)

#### Comments
- Lines starting with `//` are treated as comments
- Inline comments after `//` are also supported

## Examples

### Example 1: Simple Implication

**Input** (`test_1.ikm`):
```ikm
worlds {
    w0: P=1, Q=0, R=1, S=0
    w1: P=0, Q=1, R=1, S=0
    w2: P=1, Q=1, R=0, S=0, Z=1
}
access {
    w0: w0, w1, w2
    w1: w1, w2
    w2: w2
}
expr: !R -> Z
```

**Output**:
```
AST:
Implies
  Not
    Var(R)
  Var(Z)

Result per world:
 [1 1 1]

Kripke Matrix:
         P-0  P-1  P-2  P-3  P-4
World-0    1    0    1    0    0
World-1    0    1    1    0    0
World-2    1    1    0    0    1
```

**Interpretation**: The expression `!R -> Z` (if not R then Z) is true in all worlds according to intuitionistic semantics.

### Example 2: Modal Logic for Type Checking

**Input** (`test_2.ikm`):
```ikm
// Simulating type checking where P and Q represent initialized variables
worlds {
    w0: P=0, Q=0
    w1: P=1, Q=0
    w2: P=1, Q=1, Z=0
    w3: P=1, Q=1, Z=1
}
access {
    w0: w0, w1, w2, w3
    w1: w1, w2, w3
    w2: w2, w3
    w3: w3
}
expr: (#P && #Q) -> Z
```

**Output**:
```
AST:
Implies
  And
    Square
      Var(P)
    Square
      Var(Q)
  Var(Z)

Result per world:
 [0 0 0 1]

Kripke Matrix:
         P-0  P-1  P-2
World-0    0    0    0
World-1    1    0    0
World-2    1    1    0
World-3    1    1    1
```

**Interpretation**: The expression `(#P && #Q) -> Z` (if P and Q are necessarily true, then Z must be true) is only true in world w3, where both P and Q are necessarily true and Z is also true. This demonstrates how intuitionistic logic handles constructive implications in multi-world scenarios.

## Running Examples

To run the provided examples:

```bash
# Run example 1
cd matrix_based_kripke_model
python cli.py test_cases/test_1.ikm

# Run example 2
python cli.py test_cases/test_2.ikm
```

## Understanding the Output

### AST (Abstract Syntax Tree)
Shows the parsed structure of your logical expression, making it easy to verify that the expression was parsed correctly.

### Result per World
A numpy array showing the truth value of the expression in each world:
- `[1 1 1]` means the expression is true in all worlds
- `[0 0 0 1]` means the expression is false in the first three worlds but true in the fourth

### Kripke Matrix
A matrix representation where:
- Rows represent worlds (World-0, World-1, etc.)
- Columns represent propositional variables (P-0, P-1, etc.)
- Values are 0 (false) or 1 (true)

## Applications

### 1. Constructive Mathematics
- Verify constructive proofs
- Check intuitionistic validity of mathematical statements
- Study constructive analysis and algebra

### 2. Type Theory and Programming Languages
- Verify variable initialization patterns in functional programming
- Check resource usage patterns with constructive semantics
- Ensure proper state transitions in dependent type systems

### 3. Formal Verification
- Verify properties of concurrent systems with constructive reasoning
- Check safety and liveness properties using intuitionistic semantics
- Model checking of finite-state systems with information growth

### 4. Educational Purposes
- Learn intuitionistic logic concepts
- Understand constructive reasoning and Kripke semantics
- Practice formal reasoning without classical assumptions

## Technical Details

### Matrix Operations
The implementation uses efficient matrix operations:
- **Accessibility Matrix**: Binary matrix representing which worlds can access which other worlds
- **Valuation Matrix**: Matrix where each row represents a world and each column represents a propositional variable
- **Modal Operations**: Computed using matrix multiplication and aggregation operations

### Intuitionistic Logic Semantics
- **p → q (Implication)**: True in world w if for all worlds accessible from w, either p is false or q is true
- **¬p (Negation)**: True in world w if p is false in all worlds accessible from w
- **□φ (Necessity)**: True in world w if φ is true in all worlds accessible from w
- **◇φ (Possibility)**: True in world w if φ is true in at least one world accessible from w

### Performance
The matrix-based approach provides O(n²) complexity for most operations, where n is the number of worlds, making it suitable for models with hundreds of worlds.

## Contributing

This project is open for contributions! Areas for improvement include:
- Support for more intuitionistic logics (Heyting algebras, etc.)
- Additional constructive operators (until, since, etc.)
- GUI interface
- Performance optimizations
- More comprehensive test suite
- Integration with proof assistants (Coq, Agda, etc.)

## Acknowledgments

This implementation is based on intuitionistic Kripke semantics, with matrix-based computation techniques for efficient evaluation of constructive logic expressions.
