from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import SessionLocal

from app.models.study_record import StudyRecord
from app.models.study_goal import StudyGoal

from app.schemas.study_record import (
    StudyRecordCreate,
    StudyRecordUpdate
)

from datetime import date

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/study-records")
def get_study_records(
    db: Session = Depends(get_db)
):
    records = db.query(StudyRecord).all()

    return records

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


@router.get("/study-records/date/{study_date}")
def get_study_records_by_date(
    study_date: str,
    db: Session = Depends(get_db)
):
    records = db.query(StudyRecord).filter(
        StudyRecord.study_date == study_date
        ).all()

    return records


@router.get("/study-records/{record_id}")
def get_study_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(StudyRecord).filter(
        StudyRecord.id == record_id
    ).first()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found"
        )

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

    if update_record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found"
        )

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


@router.delete("/study-records/{record_id}")
def delete_study_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    delete_record = db.query(StudyRecord).filter(
        StudyRecord.id == record_id
    ).first()

    if delete_record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found"
        )

    db.delete(delete_record)
    db.commit()

    return {
        "message": "study record deleted"
    }

@router.get("/progress")
def get_progress(
    db: Session = Depends(get_db)
):
    total_study_time = db.query(
        func.sum(StudyRecord.study_time)
    ).scalar()

    if total_study_time is None:
        total_study_time = 0

    goal = db.query(StudyGoal).first()

    if goal is None:
        return {
            "total_study_time": total_study_time,
            "target_hours": 0,
            "achievement_rate": 0
        }

    achievement_rate = (
        total_study_time / goal.target_hours
    ) * 100

    return {
        "total_study_time": total_study_time,
        "target_hours": goal.target_hours,
        "achievement_rate": round(achievement_rate, 2)
    }

@router.get("/progress")
def get_progress(
    db: Session = Depends(get_db)
):
    records = db.query(StudyRecord).all()

    total_study_time = sum(
        record.study_time for record in records
    )

    goal_time = 2000

    achievement_rate = (
        total_study_time / goal_time
    ) * 100

    return {
        "total_study_time": total_study_time,
        "achievement_rate": achievement_rate
    }