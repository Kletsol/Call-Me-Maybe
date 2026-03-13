import json
from pydantic import BaseModel, model_validator


class FunctionError(Exception):
    pass


class ValidFunction(BaseModel):
    NAME = str
    DESCRIPTION = str
    PARAMETERS = dict[str, dict[str, str]]
    RETURNS = dict[str, str]

    @model_validator(mode='after')
    def validate(self):
        for key in self.PARAMETERS.keys():
            if 'type' not in self.PARAMETERS[key].keys():
                raise FunctionError('Unsupported argument type '
                                    f'for parameter {key} in '
                                    f'function {self.NAME}')
        return self


def get_function_def(path: str) -> list:
    try:
        with open(path, "r") as file:
            data = json.load(file)
        if len(data) == 0:
            raise FunctionError("[ERROR]: No data in functions definition file")
        function_defs = []
        for function in data:
            function_defs.append(
                ValidFunction(name=function["name"],
                              description=function["description"],
                              parameters=function["parameters"],
                              returns=function["returns"], ))
        return function_defs
    except FileNotFoundError:
        raise FileNotFoundError("[ERROR]: functions definition"
                                f"file not found in {path}")
    except PermissionError:
        raise PermissionError("[ERROR]: can't open file - permission denied")
    except json.JSONDecodeError:
        raise FunctionError("[ERROR]: can't load file - invalid json")
