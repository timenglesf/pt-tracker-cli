from typing import List


def create_list_display(list: List[str]) -> str:
    display_str = ""
    for s in list:
        display_str += f"{s}/"

    return display_str[:-1]


def argument_in_list(argument: str, list: List[str]) -> bool:
    if argument.lower() not in list:
        print(
            f"{argument} is not a valid argument please use: {create_list_display(list)}"
        )
        return False
    return True
