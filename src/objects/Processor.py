from src import ValidPrompt, ValidFunction, Model
from typing import Any


class Processor():
    def __init__(self, prompts: list, functions: list, llm: Model):
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm

    def process_prompt(self):
        # ids_list = []
        # logits_list = []
        output = []
        for prompt in self.__prompts:
            prompt_output: dict[Any, Any] = {}
            prompt_output['prompt'] = prompt.PROMPT

            function_name = self.generate_function(prompt)
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

    def generate_function(self, prompt: ValidPrompt):
        pass

    def generate_parameters(self, prompt: ValidPrompt, function: ValidFunction):
        pass


def generate_fn_name(self, prompt: ValidPrompt) -> Any:
    """ Given a prompt, returns the most useful
        function of the PromptProcessor's functions
        to solve the prompt """
    available_functions = self.get_available_functions()

    function_progress = ''
    while True:
        # Prompt creation
        prompt_message = 'Here are the different functions available: ' + \
            f'{available_functions}. ' + \
            f'To resolve the prompt, "{prompt.prompt}".'

        # Token generator
        for generation in self.__llm.predict_multiple_tokens(
            prompt_message=prompt_message,
                previous_tokens=function_progress):

            # Processing current token
            remaining_functions = []
            for function in available_functions:
                if function['name'].startswith(function_progress
                                               + generation):
                    remaining_functions.append(function)
            if (len(remaining_functions) == 1):
                return remaining_functions[0]['name']
            elif len(remaining_functions) > 1 and generation != '':
                function_progress = function_progress + generation
                available_functions = remaining_functions
                break
