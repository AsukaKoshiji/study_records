from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.study_record import StudyRecord
from app.schemas.study_record import (
    StudyRecordCreate,
    StudyRecordUpdate
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/study-records")
def create_study_record(
    record: StudyRecordCreate,
    db: Session = Depends(get_db)
):
    new_record = StudyRecord(
        title=record.title,
        content=record.content,
        study_time=record.study_time,
        study_date=record.study_date,
        memo=record.memo
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "study record created"
    }


@router.get("/study-records")
def get_study_records(
    db: Session = Depends(get_db)
):
    records = db.query(StudyRecord).all()

    return records


@router.get("/study-records/{record_id}")
def get_study_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(StudyRecord).filter(
        StudyRecord.id == record_id
    ).first()

    return record


@router.put("/study-records/{record_id}")
def update_study_record(
    record_id: int,
    record: StudyRecordUpdate,
    db: Session = Depends(get_db)
):
    update_record = db.query(StudyRecord).filter(
        StudyRecord.id == record_id
    ).first()

    update_record.title = record.title
    update_record.content = record.content
    update_record.study_time = record.study_time
    update_record.study_date = record.study_date
    update_record.memo = record.memo

    db.commit()
    db.refresh(update_record)

    return {
        "message": "study record updated"
    }