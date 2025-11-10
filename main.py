from typing import Annotated, List
import typer
from database import create_exercise, engine, Base
from helper import create_list_display, argument_in_list

ACTIONS = ["log", "display"]
EXERCISES = ["pushups", "run", "plank", "all"]


ACTIONS_HELP_DISPLAY = f"Available actions: {create_list_display(ACTIONS)}"
EXERCISES_HELP_DISPLAY = f"Available exercises: {create_list_display(EXERCISES)}"

Base.metadata.create_all(engine)


def main(
    action: Annotated[
        str,
        typer.Argument(
            help=ACTIONS_HELP_DISPLAY,
        ),
    ],
    exercise: Annotated[str, typer.Argument(help=EXERCISES_HELP_DISPLAY)],
    value: Annotated[
        int,
        typer.Option(
            help="Value of reps, time, or distance.",
        ),
    ] = 0,
):
    # Validate arguments
    if not argument_in_list(action, ACTIONS):
        typer.Exit(1)
        return
    if not argument_in_list(exercise, EXERCISES):
        typer.Exit(1)
        return

    # Convert arguments to lowercase
    action = action.lower()
    exercise = exercise.lower()

    # Main functionality
    if action == "log":
        if value == 0:
            return
        if exercise != "run":
            create_exercise(exercise, value)
    elif action == "display":
        print("Displaying exercise")
    print("Check!")
    pass


if __name__ == "__main__":
    typer.run(main)
