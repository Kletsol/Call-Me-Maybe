from src import ValidPrompt, Model, Visualizer
from typing import Any
import time

from src.parsing.functs import ValidFunction
# from time import sleep


class Processor():
    def __init__(self, prompts: list, functions: list,
                 llm: Model, visualizer: Visualizer) -> None:
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm
        self.visualizer = visualizer
        self.found = False

    def get_functions(self):
        result = []
        for function in self.__functions:
            result.append({'name': function.NAME,
                           'description': function.DESCRIPTION})
        return result

    def process_prompt(self):
        output = []
        self.visualizer.visualize()
        for prompt in self.__prompts:
            prompt_output: dict[Any, Any] = {}
            prompt_output['prompt'] = prompt.PROMPT

            function_name = self.retrieve_function_name(prompt)
            prompt_output['name'] = function_name

            parameters = self.retrieve_params(prompt, function_name)
            prompt_output['parameters'] = parameters

            self.visualizer.visualize(function_name, parameters, ring=True)
            time.sleep(4)
            self.visualizer.visualize()
            output.append(prompt_output)
        return output

    def retrieve_function_name(self, prompt: ValidPrompt):
        available_functions = self.get_functions()
        processus = ''
        while True:
            output = "Here are the functions you can access to resolve the "\
                f"prompt:{available_functions}. "\
                f"And here is the prompt: {prompt.PROMPT}"
            for token in self.__llm.generate_tokens(
                    prompt_message=output, prev_tokens=processus):
                result = []
                for function in available_functions:
                    if function['name'].startswith(processus + token):
                        result.append(function)
                if (len(result) == 1):
                    return result[0]['name']
                elif len(result) > 1 and token != '':
                    processus += token
                    available_functions = result
                    break

    def retrieve_params(self, prompt: ValidPrompt,
                        function: str) -> dict[Any, Any]:
        for funct_def in self.__functions:
            if funct_def.NAME == function:
                definition = funct_def
        output: dict = {}
        for param in definition.PARAMETERS:
            previous_gen = ''
            for arg in output.keys():
                previous_gen = previous_gen + arg +\
                    '=' + str(output[arg]) + '\n'
            previous_gen = previous_gen + param + '='
            if definition.PARAMETERS[param]['type'] == 'number':
                output[param] = self.get_nbr_param(prompt, definition,
                                                   previous_gen)
            elif definition.PARAMETERS[param]['type'] == 'string':
                output[param] = self.get_str_param(prompt, definition,
                                                   previous_gen)
        return output

    def get_nbr_param(self, prompt_message: ValidPrompt,
                      function: ValidFunction, prev_gen: str) -> int:
        output = ''
        prompt = "Here is the prompt you have to get params from: "\
            f"{prompt_message}. "\
            f"And here is the function applied on the prompt: {str(function)}"
        while True:
            for token in self.__llm.generate_tokens(
                    prompt_message=prompt, prev_tokens=prev_gen+output):
                if token == '':
                    try:
                        return output
                    except ValueError:
                        output = ''
                stop = False
                for character in token:
                    if character not in "-0123456789.\n":
                        stop = True
                if stop is True:
                    continue
                output = output + token
                if '\n' in output:
                    output = output.split('\n')[0]
                    if output is None:
                        continue
                    try:
                        return output
                    except ValueError:
                        output = ''
                break

    def get_str_param(self, prompt_message: ValidPrompt,
                      function: ValidFunction, prev_gen: str):
        output = ''
        # print(function)
        # prompt = f"{prompt_message}, {function.FULL_DEF}"
        prompt = "Here is the prompt you have to get params from: "\
            f"{prompt_message}. "\
            "And here is the function applied on the prompt: "\
            f"{function.FULL_DEF}. Keep it simple and concise."
        while "\n" not in output:
            token = self.__llm.generate_single_token(
                prompt_message=prompt, prev_tokens=prev_gen+output)
            if token == '':
                return output
            output = output + token
            if '\n' in output:
                return output.split('\n')[0].rstrip(' ')
        return output
