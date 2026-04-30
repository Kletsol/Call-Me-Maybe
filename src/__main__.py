from json import dumps
from typing import Any
import os
from src import (
    Model,
    Processor,
    Visualizer,
    parse_arguments,
    get_function_def,
    get_prompts,
)


def format_output(output: list[dict[Any, Any]]) -> str:
    json_output = dumps(output, indent=4)
    lines = json_output.splitlines()
    final_lines = []

    skip_next = 0
    for i, line in enumerate(lines):
        if skip_next > 0:
            skip_next -= 1
            continue
        if '"parameters": {' in line:
            start_indent = line.split('"parameters"')[0]
            j = i + 1
            content_parts = []
            while j < len(lines) and '}' not in lines[j]:
                content_parts.append(lines[j].strip())
                j += 1
            closing_line = lines[j]
            params_content = " ".join(content_parts)
            combined_line = f'{start_indent}"parameters": {{{params_content}}}'
            if closing_line.strip().endswith(','):
                combined_line += ','
            final_lines.append(combined_line)
            skip_next = j - i
        else:
            final_lines.append(line)
    return "\n".join(final_lines)


def main() -> None:
    try:
        args = parse_arguments()
    except Exception as e:
        print(f"\033[0;31m[ERROR]: {e}\033[0;0m")
        return

    try:
        functions = get_function_def(args.functions_definition)
    except Exception as e:
        print(f"\033[0;31m{e}\033[0;0m")
        return

    try:
        prompts = get_prompts(args.input)
    except Exception as e:
        print(f"\033[0;31m{e}\033[0;0m")
        return

    try:
        llm = Model(model_name=args.model, device=args.device)
        visual = Visualizer(active=args.visualize, ring=False)
        processor = Processor(prompts=prompts,
                              functions=functions,
                              llm=llm, visualizer=visual)
        raw_output = processor.process_prompt()
        output = format_output(raw_output)
        if args.output == args.input or \
                args.output == args.functions_definition:
            raise Exception("output file cannot be the same as "
                            "one of the input files")
        try:
            with open(args.output, "w") as file:
                file.write(output)
        except Exception:
            os.makedirs(args.output[0: str(args.output).rfind("/")])
            with open(args.output, "w") as file:
                file.write(output)
    except KeyboardInterrupt:
        print("\r\033[0;31mAborted - see you soon :D\033[0;0m")
    except Exception as e:
        print(f"\033[0;31m[ERROR]: {e}\033[0;0m")


main()
