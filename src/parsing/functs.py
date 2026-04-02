import json
from pydantic import BaseModel, model_validator


class FunctionError(Exception):
    """A custom error type for more clarity"""
    pass


class ValidFunction(BaseModel):
    """A custom verification class working with pydantic
    to ensure each function is valid"""
    NAME: str
    DESCRIPTION: str
    PARAMETERS: dict[str, dict[str, str]]
    RETURNS: dict[str, str]
    FULL_DEF: str

    @model_validator(mode="after")
    def validator(self) -> "ValidFunction":
        """Checks, after initial verification, the validity of the function

        Raises:
            FunctionError: invalid argument in function

        Returns:
            ValidFunction: self
        """
        for key in self.PARAMETERS.keys():
            if "type" not in self.PARAMETERS[key].keys():
                raise FunctionError(
                    "Unsupported argument type "
                    f"for parameter {key} in "
                    f"function {self.NAME}"
                )
        return self


def get_function_def(path: str) -> list[ValidFunction]:
    """Opens the file containing the functions definitions, verify its validity
    as well as the validity of the definitions themselves using ValidFunction

    Args:
        path (str): the path to the functions' file

    Raises:
        FunctionError: No function in file / Permission denied / invalid json
        FileNotFoundError: Given path leads nowhere

    Returns:
        list[ValidFunction]: The list extracted functions definitions
    """
    try:
        with open(path, "r") as file:
            data = json.load(file)
        if len(data) == 0:
            raise FunctionError("[ERROR]: No data in function definition file")
        function_defs = []
        for function in data:
            function_defs.append(
                ValidFunction(
                    NAME=function["name"],
                    DESCRIPTION=function["description"],
                    PARAMETERS=function["parameters"],
                    RETURNS=function["returns"],
                    FULL_DEF=str(function)
                )
            )
        return function_defs
    except FileNotFoundError:
        raise FileNotFoundError("[ERROR]: functions definition"
                                f"file not found in {path}")
    except PermissionError:
        raise FunctionError("[ERROR]: can't open file - permission denied")
    except json.JSONDecodeError:
        raise FunctionError("[ERROR]: can't load file - invalid json")
