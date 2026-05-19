from fastapi import FastAPI
from app.database.database import engine
from app.models.study_record import StudyRecord
from app.routers import study_record

StudyRecord.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(study_record.router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}