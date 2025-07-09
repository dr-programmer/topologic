import argparse
from logic_eval import parse_and_evaluate_input
from parser import pretty_print


def main():
    parser = argparse.ArgumentParser(description="Kripke Model Logic Evaluator CLI")
    parser.add_argument("input_file", type=str, help="Path to the input file with Kripke model syntax")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        input_str = f.read()

    try:
        result = parse_and_evaluate_input(input_str)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("AST:")
    pretty_print(result["ast"])
    print("\nResult per world:\n", result["result"])
    print("\nKripke Matrix:")
    result["kripke_matrix"].print()

if __name__ == "__main__":
    main() 