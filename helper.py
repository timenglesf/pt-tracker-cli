from typing import List
from datetime import datetime
from collections import namedtuple


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


def readable_datetime(dt: datetime) -> str:
    return dt.strftime("%B %d, %Y")


Time_Elapsed = namedtuple("Time_Elapsed", ["minutes", "seconds"])


def convert_seconds_to_minutes(sec: int) -> Time_Elapsed:
    return Time_Elapsed(minutes=sec // 60, seconds=sec % 60)
