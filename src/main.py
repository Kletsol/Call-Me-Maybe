from src.objects.Model import Model
from src.parsing.args import parse_arguments
from src.parsing.functs import get_function_def
from src.parsing.prompts import get_prompts


def main() -> None:
    args = parse_arguments()
    functions = get_function_def(args.functions_definition)
    prompts = get_prompts(args.input)
    llm = Model()

main()
