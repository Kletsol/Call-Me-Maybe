from src import ValidPrompt, ValidFunction, Model
from typing import Any


class Processor():
    def __init__(self, prompts: list, functions: list, llm: Model):
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm

    def get_functions(self):
        result = []
        for function in self.__functions:
            result.append({'name': function.NAME,
                           'description': function.DESCRIPTION})
        return result

    def process_prompt(self):
        # ids_list = []
        # logits_list = []
        output = []
        for prompt in self.__prompts:
            prompt_output: dict[Any, Any] = {}
            prompt_output['prompt'] = prompt.PROMPT

            function_name = self.function_generator(prompt)
            prompt_output['name'] = function_name

            parameters = self.generate_parameters(prompt, function_name)
            prompt_output['params'] = parameters

            output.append(prompt_output)
        #     id = self.__llm.encode(prompt)
        #     ids_list.append(id)
        # print(ids_list)
        # for id in ids_list:
        #     logit = self.__llm.get_logits_from_input_ids(ids_list)
        #     logits_list.append(logit)  # tolist()
        return output

    def function_generator(self, prompt: ValidPrompt):
        available_functions = self.get_functions()
        functions_str = ''
        while True:
            output = f"{available_functions}, {prompt.PROMPT}"
            for token in self.__llm.generate_multiple_tokens(
                    prompt_message=output, previous_tokens=functions_str):
                result = []
                for function in available_functions:
                    if function['name'].startswith(functions_str + token):
                        result.append(function)
                if (len(result) == 1):
                    print("\033[0;33mFound something !\033[0;0m")
                    return result[0]['name']
                elif len(result) > 1 and token != '':
                    functions_str = functions_str + token
                    available_functions = result
                    break

    def generate_parameters(self, prompt: ValidPrompt, function: ValidFunction):
        pass
