from argparse import ArgumentParser, NameSpace


def parsed_arguments() -> NameSpace:
    parser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        help="functions_definition file path",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        help="input file path",
                        default="data/input/function_calling_tests.json")
    return parser.parse_args()
