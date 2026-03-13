import json
from pydantic import BaseModel, model_validator


class PromptError(Exception):
    pass


class ValidPrompt(BaseModel):
    PROMPT: str


def get_prompts(path: str) -> list:
    try:
        with open(path, "r") as file:
            data = json.load(file)
        if len(data) == 0:
            raise PromptError("[ERROR]: No data in function calling tests")
        prompts = []
        for line in data:
            prompts.append(ValidPrompt(prompt=line["prompt"]))
        return prompts
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR]: prompts file not found in {path}")
    except PermissionError:
        raise PromptError("[ERROR]: can't open file - permission denied")
    except json.JSONDecodeError:
        raise PromptError("[ERROR]: can't load file - invalid json")