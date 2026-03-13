from argparse import ArgumentParser, NameSpace


def parse_arguments() -> NameSpace:
    parser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        help="functions_definition file path",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        help="input file path",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        help="output file path",
                        default="data/output/function_calling_results.json")
    return parser.parse_args()
