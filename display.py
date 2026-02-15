from datetime import datetime, timedelta
from typing import List

from schema import DB
from helper import readable_datetime, convert_seconds_to_minutes

NOW = datetime.now()
RANGE_INT = {
    "today": 0,
    "week": 7,
    "month": 30,
    "year": 365,
}


def today_range() -> List[datetime]:
    start = datetime.combine(NOW, datetime.min.time())
    end = datetime.combine(NOW, datetime.max.time())
    return [start, end]


def get_range(start_day: int) -> List[datetime]:
    start = datetime.combine(NOW, datetime.min.time()) - timedelta(start_day)
    end = datetime.combine(NOW, datetime.max.time())
    return [start, end]


def week_range() -> List[datetime]:
    return get_range(7)


def month_range() -> List[datetime]:
    return get_range(30)


def year_range() -> List[datetime]:
    return get_range(365)


DISPLAY_RANGES = {
    "today": today_range(),
    "week": week_range(),
    "month": month_range(),
    "year": year_range(),
}


def display_exercise(db: DB, exercise: str, range: str):
    datetime_range = DISPLAY_RANGES[range]
    start_date = datetime_range[0]
    end_date = datetime_range[1]

    display_logs = db.get_exercise(
        exercise_type=exercise, start_date=start_date, end_date=end_date
    )
    total_reps = 0
    unit = "rep"
    for e in display_logs:
        total_reps += e.value
        unit = e.unit
    if range == "today":
        if unit == "second":
            if "exercise" == "run":
                # TODO: Add distance
                print(
                    f"You ran for {display_formatted_time(total_reps)} on {readable_datetime(datetime.now())}"
                )
            else:
                verb = "planked" if exercise == "plank" else "meditated"
                print(
                    f"You {verb} for {display_formatted_time(total_reps)} on {readable_datetime(datetime.now())}"
                )
        else:
            print(
                f"You did {total_reps} {exercise} on {readable_datetime(datetime.now())}"
            )
    else:
        print(
            f"You have done {total_reps} {exercise} since {readable_datetime(start_date)}"
        )


def display_formatted_time(sec: int) -> str:
    minutes, seconds = convert_seconds_to_minutes(sec)
    if minutes == 0 and seconds > 0:
        return f"{seconds} seconds"
    elif minutes > 0 and seconds == 0:
        return f"{minutes} minutes"
    return f"{minutes} minutes and {seconds} seconds"
