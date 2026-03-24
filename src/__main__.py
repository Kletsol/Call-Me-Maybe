from src import Model, Processor, parse_arguments, get_function_def, get_prompts


def main() -> None:
    try:
        args = parse_arguments()
        functions = get_function_def(args.functions_definition)
        prompts = get_prompts(args.input)
        llm = Model(model_name=args.model, device=args.device)
        processor = Processor(prompts, functions, llm)
        output = processor.process_prompt()
        for line in output:
            print(line)
    except KeyboardInterrupt:
        print("\r\033[0;31mAborted - see you soon :D\033[0;0m")
    except Exception as e:
        print(e)


main()
