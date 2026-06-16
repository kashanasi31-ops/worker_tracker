from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Workout
from schemas import WorkoutCreate

app = FastAPI(title="Workout Tracker API")


# =========================
# 🌐 CORS FIX (IMPORTANT)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 🚀 CREATE DB ON STARTUP
# =========================
@app.on_event("startup")
def startup():
    create_db_and_tables()


# =========================
# ➕ CREATE WORKOUT
# =========================
@app.post("/workouts", response_model=Workout)
def create_workout(workout: WorkoutCreate, session: Session = Depends(get_session)):
    db_workout = Workout(**workout.model_dump())
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    return db_workout


# =========================
# 📋 GET ALL WORKOUTS
# =========================
@app.get("/workouts", response_model=list[Workout])
def get_workouts(session: Session = Depends(get_session)):
    return session.exec(select(Workout)).all()


# =========================
# 🔍 GET WORKOUT BY ID
# =========================
@app.get("/workouts/{workout_id}", response_model=Workout)
def get_workout(workout_id: int, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


# =========================
# ✏️ UPDATE WORKOUT
# =========================
@app.put("/workouts/{workout_id}", response_model=Workout)
def update_workout(workout_id: int, data: WorkoutCreate, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    for key, value in data.model_dump().items():
        setattr(workout, key, value)

    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout


# =========================
#DELETE WORKOUT
# =========================
@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    session.delete(workout)
    session.commit()

    return {"message": "Workout deleted successfully"}