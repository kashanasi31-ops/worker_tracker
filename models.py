from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise: str
    sets: int
    reps: int
    weight_kg: float
    date: date
    notes: Optional[str] = None