from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy import Engine, String, between, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    mapped_column,
    Mapped,
)


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


class DB:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def insert_exercise(self, exercise_type: str, value: int):
        with Session(self.engine) as session:
            new_exercise = Exercise(
                date=datetime.now(),
                exercise=exercise_type,
                value=value,
            )
            session.add(new_exercise)
            session.commit()
            session.refresh(new_exercise)
        pass

    def insert_run(self, exercise_type: str, value: int, distance: float):
        with Session(self.engine) as session:
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

    #
    def get_exercise(
        self, exercise_type: str, start_date: datetime, end_date: datetime
    ) -> Sequence[Exercise]:
        start = datetime.combine(start_date, datetime.min.time())
        end = datetime.combine(end_date, datetime.max.time())
        with Session(self.engine) as session:
            # Get Exercise from some date
            stmt = select(Exercise).where(
                Exercise.exercise == exercise_type,
                between(Exercise.date, start, end),
            )
            results = session.scalars(stmt).all()
        return results
