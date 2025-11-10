from datetime import datetime, date, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select
import sqlalchemy
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    mapped_column,
    Mapped,
    Session,
    relationship,
)

engine = create_engine("sqlite:///db.sqlite")


class Base(DeclarativeBase):
    pass


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    exercise: Mapped[str] = mapped_column(String(10))
    value: Mapped[int]
    distance: Mapped[Optional[float]]

    def __repr__(self) -> str:
        return f"Exercise(id={self.id}, date={self.date}, exercise={self.exercise}, value={self.value})"


def create_exercise(exercise_type: str, value: int):
    with Session(engine) as session:
        new_exercise = Exercise(
            date=datetime.now(),
            exercise=exercise_type,
            value=value,
        )
        session.add(new_exercise)
        session.commit()
        session.refresh(new_exercise)
    pass


def create_run(exercise_type: str, value: int, distance: float):
    with Session(engine) as session:
        new_exercise = Exercise(
            date=datetime.now(),
            exercise=exercise_type,
            value=value,
            distance=distance,
        )
        session.add(new_exercise)
        session.commit()
        session.refresh(new_exercise)
    pass
