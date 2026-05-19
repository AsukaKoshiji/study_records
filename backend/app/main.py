from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.study_record import StudyRecord
from app.routers import study_record
from app.routers.study_record import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}