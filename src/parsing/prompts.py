import json
from typing import Any
from pydantic import BaseModel


class PromptError(Exception):
    """A custom error type for more clarity"""
    pass


class ValidPrompt(BaseModel):
    """A custom verification class working with pydantic
    to ensure each prompt is valid"""
    PROMPT: str


def duplicate_key(pairs: ((list[tuple[Any, Any]]))) -> Any:
    result = {}
    for key, value in pairs:
        if key in result:
            raise PromptError(f"[ERROR]: duplicate key '{key}' in function")
        result[key] = value
    return result


def get_prompts(path: str) -> list[ValidPrompt]:
    """
    Opens the file containing the prompts to process, verify its validity
    as well as the validity of the prompts themselves using ValidPrompt

    Args:
        path (str): the path to the prompts' file

    Raises:
        PromptError: No prompt found in file / Permission denied / invalid json
        FileNotFoundError: Given path leads nowhere

    Returns:
        list[ValidPrompt]: The list of extracted prompts
    """
    try:
        with open(path, "r") as file:
            data = json.load(file, object_pairs_hook=duplicate_key)
        if len(data) == 0:
            raise PromptError("[ERROR]: No data in function calling tests")
        for prompt in data:
            for key in prompt.keys():
                if key != 'prompt':
                    raise PromptError(f"[ERROR]: Invalid field '{key}' "
                                      "in prompt definition")
        prompts = []
        for line in data:
            if line['prompt'] == "":
                raise PromptError("[ERROR]: empty prompt in file")
            prompts.append(ValidPrompt(PROMPT=line["prompt"]))
        return prompts
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR]: prompts file not found in {path}")
    except PermissionError:
        raise PromptError("[ERROR]: can't open file - permission denied")
    except json.JSONDecodeError:
        raise PromptError("[ERROR]: can't load file - invalid json")
