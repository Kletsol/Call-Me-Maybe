from src import ValidPrompt, Model
from typing import Any

from src.parsing.functs import ValidFunction
# from time import sleep


class Processor():
    def __init__(self, prompts: list, functions: list, llm: Model):
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm

    # @staticmethod
    # def animation():
    #     string = ["🤔 ", ".", ".", ".", ".", ".", ".",
    # "\033[0;33mFound something !\033[0;0m💡"]
    #     for step in string:
    #         print(step, end="")
    #         sleep(1)
    #     print()

    def get_functions(self):
        result = []
        for function in self.__functions:
            result.append({'name': function.NAME,
                           'description': function.DESCRIPTION})
        return result

    def process_prompt(self):
        output = []
        for prompt in self.__prompts:
            prompt_output: dict[Any, Any] = {}
            prompt_output['prompt'] = prompt.PROMPT

            function_name = self.function_generator(prompt)
            prompt_output['name'] = function_name

            parameters = self.params_generator(prompt, function_name)
            prompt_output['params'] = parameters

            output.append(prompt_output)
        return output

    def function_generator(self, prompt: ValidPrompt):
        available_functions = self.get_functions()
        functions_str = ''
        while True:
            output = f"{available_functions}, {prompt.PROMPT}"
            for token in self.__llm.generate_tokens(
                    prompt_message=output, previous_tokens=functions_str):
                result = []
                for function in available_functions:
                    if function['name'].startswith(functions_str + token):
                        result.append(function)
                if (len(result) == 1):
                    print("🤔 ...... \033[0;33mFound something !\033[0;0m💡")
                    # self.animation()
                    return result[0]['name']
                elif len(result) > 1 and token != '':
                    functions_str = functions_str + token
                    available_functions = result
                    break

    def params_generator(self, prompt: ValidPrompt,
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
                output[param] = self.nbr_param_generator(prompt, definition, previous_gen)
            elif definition.PARAMETERS[param]['type'] == 'string':
                output[param] = self.str_param_generator(prompt, definition, previous_gen)
        return output

    def nbr_param_generator(self, prompt_message: ValidPrompt, function: ValidFunction, previous_gen: str) -> int:
        output = ''
        numbers = "-0123456789"
        prompt = f"{prompt_message}, {function}"
        while True:
            for token in self.__llm.generate_tokens(prompt_message=prompt, previous_tokens=previous_gen):
                for character in token:
                    if character not in numbers:
                        continue
                    else:
                        output = output + token
                if output:
                    return output


    def str_param_generator(self, prompt: ValidPrompt, function: ValidFunction, previous_gen: str):
        pass
