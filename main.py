from typing import Annotated
import typer
from sqlalchemy import create_engine

# local imports
import display
from schema import DB, Base
from helper import create_list_display, argument_in_list


ACTIONS = ["log", "display"]
EXERCISES = ["pushups", "run", "plank", "all"]


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
    value: Annotated[
        int,
        typer.Option(
            help="Value of reps, time, or distance.",
        ),
    ] = 0,
    range: Annotated[
        str,
        typer.Option(
            help="Display logged exercise data: today/week/month/year/all",
        ),
    ] = "today",
):
    # Create Connection to sqlite
    engine = create_engine("sqlite:///db.sqlite")
    Base.metadata.create_all(engine)

    db = DB(engine)

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
            db.insert_exercise(exercise, value)
    elif action == "display":
        display_range_str = list(display.DISPLAY_RANGES.keys())
        if not argument_in_list(range, display_range_str):
            typer.Exit(1)
            return
        display.display_exercise(db, exercise, range)


if __name__ == "__main__":
    typer.run(main)
