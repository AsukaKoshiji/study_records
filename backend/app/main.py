from fastapi import FastAPI

from app.database.database import engine, Base

from app.models.study_record import StudyRecord
from app.models.study_goal import StudyGoal

from app.routers import study_record
from app.routers import study_goal

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(study_record.router)
app.include_router(study_goal.router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}