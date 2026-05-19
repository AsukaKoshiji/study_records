from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.study_record import StudyRecord
from app.schemas.study_record import StudyRecordCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/study-records/")
def create_study_record(
    record: StudyRecordCreate,
    db: Session = Depends(get_db)
):
    db_record = StudyRecord(
        title=record.title,
        content=record.content,
        study_time=record.study_time,
        study_date=record.study_date,
        memo=record.memo
    )

    db.add(new_record)
    db.commit()
    db.refredh(new_record)

    return {
        "message": "study record created"
        }