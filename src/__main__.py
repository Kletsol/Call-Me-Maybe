from torch import softmax

from src import Model
from src.objects.Processor import Processor
from src.parsing.args import parse_arguments
from src.parsing.functs import get_function_def
from src.parsing.prompts import get_prompts


def main() -> None:
    try:
        args = parse_arguments()
        functions = get_function_def(args.functions_definition)
        prompts = get_prompts(args.input)
        temp_prompts = []
        temp_functions = []
        for prompt in prompts:
            temp_prompts.append(prompt.PROMPT)
        for function in functions:
            temp_functions.append(function.NAME)
        llm = Model(model_name=args.model, device=args.device)
        processor = Processor(temp_prompts, temp_functions, llm)
        print(processor.process_prompt())
    except Exception as e:
        print(e)


main()
# softmax()
