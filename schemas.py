from pydantic import BaseModel
from datetime import date


class WorkoutCreate(BaseModel):
    exercise: str
    sets: int
    reps: int
    weight_kg: float
    date: date
    notes: str | None = None