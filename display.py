from datetime import datetime

from schema import DB
from helper import readable_datetime


def log_today(exercise: str, db: DB):
    display_logs = db.get_exercise(
        exercise_type=exercise,
        start_date=datetime.now(),
        end_date=datetime.now(),
    )
    total_reps = 0
    for e in display_logs:
        total_reps += e.value
    print(f"You did {total_reps} {exercise} on {readable_datetime(datetime.now())}")
