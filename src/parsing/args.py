from argparse import ArgumentParser, NameSpace


def parse_arguments() -> NameSpace:
    parser = ArgumentParser()
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
    parsed = parser.parse_args()
    return parsed
