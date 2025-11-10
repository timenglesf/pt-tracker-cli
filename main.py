from typing import Annotated, List
import typer

ACTIONS = ["log", "display"]
EXERCISES = ["pushups", "run", "plank", "all"]


def create_list_display(list: List[str]) -> str:
    display_str = ""
    for s in list:
        display_str += f"{s}/"

    return display_str[:-1]


ACTIONS_HELP_DISPLAY = f"Available actions: {create_list_display(ACTIONS)}"
EXERCISES_HELP_DISPLAY = f"Available exercises: {create_list_display(EXERCISES)}"


def main(
    action: Annotated[
        str,
        typer.Argument(
            help=ACTIONS_HELP_DISPLAY,
        ),
    ],
    exercise: Annotated[str, typer.Argument(help=EXERCISES_HELP_DISPLAY)],
):
    if action.lower() not in ACTIONS:
        print(
            f"{action} is not an available action please use: {create_list_display(ACTIONS)}"
        )
        typer.Exit(1)
        return
    action = action.lower()
    exercise = exercise.lower()
    if action == "log":
        print("Logging exercise")
        print("exercise")
    elif action == "display":
        print("Displaying exercise")
    print("Check!")
    pass


if __name__ == "__main__":
    typer.run(main)
