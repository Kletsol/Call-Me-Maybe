from typing import Optional, Any

class Visualizer:
    def __init__(self, active: bool):
        self.active = active

    @staticmethod
    def get_spaces(total: int, value: int) -> str:
        spaces: str = ''
        difference = total - value
        for i in range(difference):
            spaces = spaces + " "
        return spaces

    def visualize(self, function: Optional[str] = None, params: Optional[dict[Any, Any]] = None, result: str = '', ring: bool = False):
        print("\033[H\033[J", end="")
        header = "\033[0;33m╔════════════════════════════════════════════════"\
            "════════════════════════════════════════════════════╗\033[0;0m"
        footer = "\033[0;33m╚════════════════════════════════════════════════"\
            "════════════════════════════════════════════════════╝\033[0;0m"
        title = ["\033[1m   __  __                  __         __      _    __\033[22m",
                 "\033[1m  /   /__\\ |   |     |\\/| |__   |\\/| /__\\ \\/ |_}  |__\033[22m",
                 "\033[1m  \\__ |  | |__ |__   |  | |__   |  | |  | /  |__} |__\033[22m"]
        name = ["    Catched a function name:",
                f"    - {function}"]
        parameters = ["    Got parameters:",
                      f"    - {params}"]
        space = self.get_spaces(60, 0)
        print(header)
        count = 0
        for i in range(27):
            if ring is False:
                if i < 9 or count > 16:
                    print(
                        "\033[0;33m║                                         "
                        "                                                "
                        "           ║\033[0;0m"
                    )
                else:
                    middle = [
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
                    if i >= 12 and i <= 14:
                        middle[count] = middle[count] + title[i - 12]
                        space = "       "
                    print(
                        f"\033[0;33m║\033[0;0m    \033[0;34m{middle[count]}"
                        f"\033[0;0m{space}\033[0;33m║\033[0;0m"
                    )
                    space = self.get_spaces(60, 0)
                    count += 1
            else:
                if count > 25:
                    print(
                        "\033[0;33m║                                         "
                        "                                                    "
                        "       ║\033[0;0m"
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
                    if i >= 12 and i <= 14:
                        middle[count] = middle[count] + title[i - 12]
                        space = "       "

                    if i >= 17 and i <= 18:
                        middle[count] = middle[count] + name[i - 17]
                        space = self.get_spaces(60, len(name[i - 17]))

                    if i >= 21 and i <= 22:
                        if i == 22 and len(parameters[1]) > 60:
                            middle[count] = middle[count] + "      Too many parameters, we'll send you an e-mail"
                            space = "         "
                        else:
                            middle[count] = middle[count] + parameters[i - 21]
                            space = self.get_spaces(60, len(parameters[i - 21]))

                    print(
                        f"\033[0;33m║\033[0;0m    \033[0;34m{middle[count]}"
                        f"\033[0;0m{space}\033[0;33m║\033[0;0m"
                    )
                    space = self.get_spaces(60, 0)
                    count += 1
            self.ring = False
        print(footer)
