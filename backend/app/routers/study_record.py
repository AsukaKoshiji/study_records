from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.study_goal import StudyGoal
from backend.app.models.study_record import StudyRecord
from backend.app.schemas.study_record import (
    StudyRecordCreate,
    StudyRecordUpdate,
)

router = APIRouter()


# =========================================================
# DB Dependency
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# GET /api/study-records
# =========================================================

@router.get("/")
def get_study_records(
    db: Session = Depends(get_db),
):
    return db.query(StudyRecord).all()


# =========================================================
# POST /api/study-records
# =========================================================

@router.post("/", status_code=201)
def create_study_record(
    record: StudyRecordCreate,
    db: Session = Depends(get_db),
):
    new_record = StudyRecord(
        **record.model_dump()
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# =========================================================
# GET /api/study-records/date/{study_date}
# =========================================================

@router.get("/date/{study_date}")
def get_study_records_by_date(
    study_date: date,
    db: Session = Depends(get_db),
):
    return (
        db.query(StudyRecord)
        .filter(StudyRecord.study_date == study_date)
        .all()
    )


# =========================================================
# GET /api/study-records/{record_id}
# =========================================================

@router.get("/{record_id}")
def get_study_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(StudyRecord)
        .filter(StudyRecord.id == record_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found",
        )

    return record


# =========================================================
# PUT /api/study-records/{record_id}
# =========================================================

@router.put("/{record_id}")
def update_study_record(
    record_id: int,
    record: StudyRecordUpdate,
    db: Session = Depends(get_db),
):
    update_record = (
        db.query(StudyRecord)
        .filter(StudyRecord.id == record_id)
        .first()
    )

    if update_record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found",
        )

    for key, value in (
        record.model_dump(exclude_unset=True).items()
    ):
        setattr(update_record, key, value)

    db.commit()
    db.refresh(update_record)

    return update_record


# =========================================================
# DELETE /api/study-records/{record_id}
# =========================================================

@router.delete("/{record_id}")
def delete_study_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    delete_record = (
        db.query(StudyRecord)
        .filter(StudyRecord.id == record_id)
        .first()
    )

    if delete_record is None:
        raise HTTPException(
            status_code=404,
            detail="Study record not found",
        )

    db.delete(delete_record)
    db.commit()

    return {
        "message": "study record deleted"
    }


# =========================================================
# GET /api/study-records/progress
# =========================================================

@router.get("/progress")
def get_progress(
    db: Session = Depends(get_db),
):
    total_study_time = (
        db.query(func.sum(StudyRecord.study_time))
        .scalar()
        or 0
    )

    goal = db.query(StudyGoal).first()

    if goal is None or goal.target_hours == 0:
        return {
            "total_study_time": total_study_time,
            "target_hours": 0,
            "achievement_rate": 0.0,
        }

    achievement_rate = (
        total_study_time / goal.target_hours
    ) * 100

    return {
        "total_study_time": total_study_time,
        "target_hours": goal.target_hours,
        "achievement_rate": round(
            achievement_rate,
            2,
        ),
    }