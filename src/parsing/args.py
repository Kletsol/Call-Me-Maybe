from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """
    Parses arguments given at execution using argparse

    Returns:
        Namespace: the parsed arguments
    """
    parser = ArgumentParser(exit_on_error=False)
    parser.add_argument("--functions_definition",
                        help="functions_definition file path",
                        default="data/input/functions_definition.json",
                        required=False)
    parser.add_argument("--input",
                        help="input file path",
                        default="data/input/function_calling_tests.json",
                        required=False)
    parser.add_argument("--output",
                        help="output file path",
                        default="data/output/function_calling_results.json",
                        required=False)
    parser.add_argument("--model",
                        help="model name",
                        default="Qwen/Qwen3-0.6B",
                        required=False)
    parser.add_argument("--device",
                        help="computation device",
                        default=None,
                        required=False)
    parser.add_argument("--visualize",
                        help="activate visualizer",
                        action="store_true",
                        required=False)
    parsed = parser.parse_args()
    return parsed
