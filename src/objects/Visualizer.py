from typing import Optional, Any


class Visualizer:
    """
    A class whose role is to generate the graphical rendering of the project
    """
    def __init__(self, active: bool):
        """
        Initiates class-internal parameters

        Args:
            active (bool): set to True if you want to visualize the
            project, False otherwise
        """
        self.active = active

    @staticmethod
    def get_spaces(total: int, value: int) -> str:
        """
        Calculates the number of spaces needed depending on a
        total length and a value to substract to it. Used in visualize()
        to get the correct amount of spaces after a variable

        Args:
            total (int): The base number of spaces
            value (int): The length of the variable

        Returns:
            str: a string containing the calculated amount of spaces
        """
        spaces: str = ''
        difference = total - value
        for i in range(difference):
            spaces = spaces + " "
        return spaces

    @staticmethod
    def format_params(parameters: dict[Any, Any]) -> list[str]:
        """
        Formats the given parameters as a list of strings

        Args:
            parameters (dict[Any, Any]): The parameters to format

        Returns:
            list[str]: The formatted parameters
        """
        output = ["    Got parameters:"]
        for key, value in parameters.items():
            output.append(f"    - {key}: {value}")
        return output

    @staticmethod
    def format_prompt(prompt: str) -> list[str]:
        """
        Formats the given prompt as a list of strings

        Args:
            prompt (str): The prompt to format

        Returns:
            list[str]: The formatted prompt
        """
        size = len(prompt)
        if prompt == "Nothing left to process":
            output = [f"    {prompt}"]
            return output
        output = ["    Processing prompt:"]
        if size > 52:
            start, end = prompt[:52], prompt[52:]
            output.append(f"    - {start}")
            output.append(f"      {end}")
        else:
            output.append(f"    - {prompt}")
        return output

    def visualize(self, prompt: str = '', function: Optional[str]
                  = None, params: Optional[dict[Any, Any]] = None,
                  ring: bool = False) -> None:
        """
        Manages the graphical render of the project over time.

        Args:
            prompt (str, optional): The prompt to display. Defaults to ''.
            function (Optional[str], optional): The function to display.
            Defaults to None.
            params (Optional[dict[Any, Any]], optional): The parameters to
            display. Defaults to None.
            ring (bool, optional): True if the phone must ring, Fase otherwise.
            Defaults to False.
        """
        print("\033[H\033[J", end="")

        header = "\033[0;33m╔════════════════════════════[Created with waaaay"\
            " too much time by lbonnet]════════════════════════════╗\033[0;0m"

        footer = "\033[0;33m╚════════════════════════════════════════════════"\
            "══════════════════════════════════════════════════════╝\033[0;0m"

        title = ["     \033[1;35m__  __                  \033[1;33m__         "
                 "\033[1;35m__      _    __\033[22m",
                 "    \033[1;35m/   /__\\ |   |     \033[1;33m|\\/| |__   "
                 "\033[1;35m|\\/| /__\\ \\/ |_}  |__\033[22m",
                 "    \033[1;35m\\__ |  | |__ |__   \033[1;33m|  | |__   "
                 "\033[1;35m|  | |  | /  |__} |__\033[22m"]
        if prompt != '':
            prompt_lines = self.format_prompt(prompt)

        name = ["    Catched a function name:",
                f"    - {function}"]
        if params:
            parameters = self.format_params(params)

        space = self.get_spaces(62, 0)

        print(header)
        count = 0
        for i in range(27):
            if ring is False:
                if i < 8 or count > 17:
                    print(
                        "\033[0;33m║                                         "
                        "                                                  "
                        "           ║\033[0;0m"
                    )
                else:
                    middle = [
                        "                                    ",
                        "   _.===========================._  ",
                        "  /.===========================._/\\ ",
                        " /      ___________________      \\/ ",
                        "[      /    /||/    ||/ /\\ \\      ] ",
                        " \\____/    +#+#+#+#+#+#+  \\ \\____/  ",
                        "          +#           #+  \\        ",
                        "         +#      0      #+  \\       ",
                        "        +#   1       9   #+  \\      ",
                        "       +#  2           8  #+ /      ",
                        "      +#         ●         #+       ",
                        "       +#  3           7  #+        ",
                        "        +#   4       6   #+         ",
                        "         +#      5      #+          ",
                        "       ___+#           #+______     ",
                        "      /    +#+#+#+#+#+#+      /|    ",
                        "     /______//_______\\\\______/ /    ",
                        "     [_______________________]/     ",
                    ]
                    if i >= 8 and i <= 10:
                        middle[count] = middle[count] + title[i - 8]
                        space = "       "
                    if i >= 13 and i <= (12 + len(prompt_lines)):
                        middle[count] = middle[count] + prompt_lines[i - 13]
                        space = self.get_spaces(62, len(prompt_lines[i - 13]))
                    print(
                        f"\033[0;33m║\033[0;0m    \033[0;34m{middle[count]}"
                        f"\033[0;0m{space}\033[0;33m║\033[0;0m"
                    )
                    space = self.get_spaces(62, 0)
                    count += 1
            else:
                if count > 25:
                    print(
                        "\033[0;33m║                                         "
                        "                                                    "
                        "         ║\033[0;0m"
                    )
                else:
                    middle = [
                        "            _____                   ",
                        "           /____/\\                  ",
                        "          /     \\/                  ",
                        "         /       ]                  ",
                        "        /    ___/                   ",
                        "       /    /                       ",
                        "      /    /     \033[1mDRIIIING !\033[22m         ",
                        "     /    /                         ",
                        "    /    /    \033[1mDRIIIIIIIIIING !!!\033[22m    ",
                        "   /    /                           ",
                        "  /    /\\                           ",
                        " /     \\/    _||_____||__           ",
                        "|       ]   /||/    ||/ /\\          ",
                        " \\_____/   +#+#+#+#+#+#+  \\         ",
                        "          +#           #+  \\        ",
                        "         +#      0      #+  \\       ",
                        "        +#   1       9   #+  \\      ",
                        "       +#  2           8  #+ /      ",
                        "      +#         ●         #+       ",
                        "       +#  3           7  #+        ",
                        "        +#   4       6   #+         ",
                        "         +#      5      #+          ",
                        "       ___+#           #+______     ",
                        "      /    +#+#+#+#+#+#+      /|    ",
                        "     /______//_______\\\\______/ /    ",
                        "     [_______________________]/     ",
                    ]
                    if i >= 8 and i <= 10:
                        middle[count] = middle[count] + title[i - 8]
                        space = "       "

                    if i >= 13 and i <= (12 + len(prompt_lines)):
                        middle[count] = middle[count] + prompt_lines[i - 13]
                        space = self.get_spaces(62, len(prompt_lines[i - 13]))

                    if i >= 17 and i <= 18:
                        middle[count] = middle[count] + name[i - 17]
                        space = self.get_spaces(62, len(name[i - 17]))

                    if i >= 20 and i <= (19 + len(parameters)):
                        middle[count] = middle[count] + parameters[i - 20]
                        space = self.get_spaces(62, len(parameters[i - 20]))

                    print(
                        f"\033[0;33m║\033[0;0m    \033[0;34m{middle[count]}"
                        f"\033[0;0m{space}\033[0;33m║\033[0;0m"
                    )
                    space = self.get_spaces(62, 0)
                    count += 1
            self.ring = False
        print(footer)
