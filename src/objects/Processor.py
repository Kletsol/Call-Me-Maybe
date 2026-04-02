from src import ValidPrompt, Model, Visualizer
from typing import Any
import time

from src.parsing.functs import ValidFunction


class Processor():
    """The main class to process the prompt, retrieve correct
    function and parameters and return it
    """
    def __init__(self, prompts: list[ValidPrompt],
                 functions: list[ValidFunction],
                 llm: Model, visualizer: Visualizer) -> None:
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm
        self.visualizer = visualizer
        self.found = False

    def get_functions(self) -> list[dict[str, str]]:
        """
        Gets the existing functions and returns it as a list of dicts
        each dict corresponding to a function

        Returns:
            list[dict[str, str]]: The list of functions
        """
        result = []
        for function in self.__functions:
            result.append({'name': function.NAME,
                           'description': function.DESCRIPTION})
        return result

    def process_prompt(self) -> list[dict[Any, Any]]:
        """Processes each prompt in self.__prompts, looking for the
        correponding function and parameters

        Returns:
            list[dict[Any, Any]]: A list containing, for each
            processed prompt, the prompt itself, the function name
            and the parameters
        """
        output = []
        for prompt in self.__prompts:
            if self.visualizer.active is True:
                self.visualizer.visualize(prompt=prompt.PROMPT)
            prompt_output: dict[Any, Any] = {}
            prompt_output['prompt'] = prompt.PROMPT

            function_name = self.retrieve_function_name(prompt)
            prompt_output['name'] = function_name

            parameters = self.retrieve_params(prompt, function_name)
            prompt_output['parameters'] = parameters

            if self.visualizer.active is True:
                self.visualizer.visualize(prompt.PROMPT, function_name,
                                          parameters, ring=True)
                time.sleep(4)
                self.visualizer.visualize(prompt='Nothing left to process')
            output.append(prompt_output)
        return output

    def retrieve_function_name(self, prompt: ValidPrompt) -> str:
        """
        Sends a prompt depending on the available functions and the
        original prompt to the LLM, then uses constrained decoding to filter
        and extract a valid function name

        Args:
            prompt (ValidPrompt): The original prompt

        Returns:
            str: The function's name
        """
        available_functions = self.get_functions()
        processus = ''
        while True:
            output = "Here are the functions you can access to resolve the "\
                f"prompt:{available_functions}. "\
                f"And here is the prompt: {prompt.PROMPT}"
            for token in self.__llm.generate_tokens(
                    prompt=output, history=processus):
                result = []
                for function in available_functions:
                    if function['name'].startswith(processus + token):
                        result.append(function)
                if (len(result) == 1):
                    return str(result[0]['name'])
                elif len(result) > 1 and token != '':
                    processus += token
                    available_functions = result
                    break

    def retrieve_params(self, prompt: ValidPrompt,
                        function: str) -> dict[Any, Any]:
        """
        Filters the expected paramaters by type, and calls the correct
        function depending on it, then stores all the resulting parameters

        Args:
            prompt (ValidPrompt): The original prompt
            function (str): The previously catched function name

        Returns:
            dict[Any, Any]: A dict containing the parameters
        """
        for funct_def in self.__functions:
            if funct_def.NAME == function:
                definition = funct_def
        output: dict[Any, Any] = {}
        for param in definition.PARAMETERS:
            history = ''
            for arg in output.keys():
                history += arg + '=' + str(output[arg]) + '\n'
            history += param + '='
            if definition.PARAMETERS[param]['type'] == 'number':
                output[param] = self.get_nbr_param(prompt, definition,
                                                   history)
            elif definition.PARAMETERS[param]['type'] == 'string':
                output[param] = self.get_str_param(prompt, definition,
                                                   history)
        return output

    def get_nbr_param(self, prompt: ValidPrompt,
                      function: ValidFunction, history: str) -> float:
        """
        Sends a prompt depending on the original prompt and the
        function previously catched to the LLM, then uses constrained decoding
        to filter and extract a valid int parameter

        Args:
            prompt (ValidPrompt): The original prompt
            function (ValidFunction): The function previously catched
            history (str): The previously processed parameters

        Returns:
            str: The integer in the form of a string
        """
        output = ''
        prompt_to_process = "Here is the prompt you have to get params from: "\
            f"{prompt}. "\
            f"And here is the function applied on the prompt: {str(function)}"
        while True:
            for token in self.__llm.generate_tokens(
                    prompt=prompt_to_process, history=history+output):
                if token == '':
                    try:
                        return float(output)
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
                        return float(output)
                    except ValueError:
                        output = ''
                break

    def get_str_param(self, prompt: ValidPrompt,
                      function: ValidFunction, history: str) -> str:
        """
        Sends a prompt depending on the original prompt and the
        function previously catched to the LLM, then uses constrained decoding
        to filter and extract a string, being the expected parameter

        Args:
            prompt (ValidPrompt): The original prompt
            function (ValidFunction): The function previously catched
            history (str): The previously processed parameters

        Returns:
            str: The valid parameter
        """
        output = ''
        prompt_to_process = "Here is the prompt you have to get params from: "\
            f"{prompt}. "\
            "And here is the function applied on the prompt: "\
            f"{function.FULL_DEF}. Keep it simple and concise."

        while "\n" not in output:
            token = self.__llm.generate_single_token(
                prompt=prompt_to_process, history=history+output)
            if token == '':
                return output
            output = output + token
            if output not in prompt.PROMPT and output.lower() in prompt.PROMPT:
                output = output.lower()
            if '\n' in output:
                return output.split('\n')[0].rstrip(' ').strip('.*')
        return output
