from typing import Annotated, Optional

import typer
from sqlalchemy import create_engine

# Local imports
import display
from schema import DB, Base
from helper import create_list_display, argument_in_list

# -------------------------------------------------------------------
# CLI configuration (allowed commands / values)
# -------------------------------------------------------------------

ACTIONS = ["log", "display"]
EXERCISES = [
    "meditate",
    "pushups",
    "plank",
    "run",
    "situps",
    "squats",
    "all",
]

# Pre-rendered help strings for Typer (makes `--help` nicer)
ACTIONS_HELP_DISPLAY = f"Available actions: {create_list_display(ACTIONS)}"
EXERCISES_HELP_DISPLAY = f"Available exercises: {create_list_display(EXERCISES)}"


def main(
    # ----------------------------------------------------------------
    # Positional arguments
    # ----------------------------------------------------------------
    action: Annotated[
        str,
        typer.Argument(help=ACTIONS_HELP_DISPLAY),
    ],
    exercise: Annotated[
        str,
        typer.Argument(help=EXERCISES_HELP_DISPLAY),
    ],
    # ----------------------------------------------------------------
    # Options (flags)
    # ----------------------------------------------------------------
    value: Annotated[
        int,
        typer.Option(help="Value of reps, time, or distance."),
    ] = 0,
    range: Annotated[
        str,
        typer.Option(help="Display logged exercise data: today/week/month/year/all"),
    ] = "today",
    distance: Annotated[
        float,
        typer.Option(help="The distance ran, required for average pace"),
    ] = 0,
    note: Annotated[
        bool,
        typer.Option("--note", help="Add a note (prompts after Enter)."),
    ] = False,
    display_json: Annotated[
        bool, typer.Option("--json", help="Display exercises in JSON format.")
    ] = False,
):
    # ----------------------------------------------------------------
    # Database setup
    #   - Create engine
    #   - Ensure tables exist
    #   - Create DB helper instance
    # ----------------------------------------------------------------
    engine = create_engine("sqlite:///db.sqlite")
    Base.metadata.create_all(engine)
    db = DB(engine)

    # ----------------------------------------------------------------
    # Normalize input
    #   - Lowercase so user can type "Log", "RUN", etc.
    # ----------------------------------------------------------------
    action = action.lower()
    exercise = exercise.lower()

    # ----------------------------------------------------------------
    # Validate input
    #   - Exit with status code 1 if invalid
    # ----------------------------------------------------------------
    if not argument_in_list(action, ACTIONS):
        raise typer.Exit(1)
    if not argument_in_list(exercise, EXERCISES):
        raise typer.Exit(1)

    # ----------------------------------------------------------------
    # Action: log
    #   - Optional note prompt when `--note` is provided
    #   - Special handling for `run` (value OR distance allowed)
    #   - Non-run exercises require `--value`
    # ----------------------------------------------------------------
    if action == "log":
        # Prompt for note only when the user opts in with `--note`
        note_text: Optional[str] = None
        if note:
            note_text = typer.prompt(
                "Note (press Enter to finish)",
                default="",
                show_default=False,
            ).strip()

            # Convert empty string to None so DB stores "no note" cleanly
            if note_text == "":
                note_text = None

        # Special case: run logs can be saved with either value or distance
        if exercise == "run":
            if value == 0 and distance == 0:
                typer.echo("Must include a value or distance with run!")
                raise typer.Exit(1)

            db.insert_run(exercise, value, distance, note=note_text)
            return

        # All other exercises require a value
        if value == 0:
            typer.echo("Value is required (use --value).")
            raise typer.Exit(1)

        db.insert_exercise(exercise, value, note=note_text)

    # ----------------------------------------------------------------
    # Action: display
    #   - Validate range
    #   - Delegate to your display module
    # ----------------------------------------------------------------
    elif action == "display":
        display_range_str = list(display.DISPLAY_RANGES.keys())
        if not argument_in_list(range, display_range_str):
            raise typer.Exit(1)

        if display_json:
            display.display_exercise_json(
                db=db,
                exercise=exercise,
                range=range,
            )

        display.display_exercise(db, exercise, range)


# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------
if __name__ == "__main__":
    typer.run(main)
