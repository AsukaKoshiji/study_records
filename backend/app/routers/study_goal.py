from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.study_goal import StudyGoal
from app.schemas.study_goal import (
    StudyGoalCreate, 
    StudyGoalUpdate
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/study-goals")
def create_study_goal(
    goal: StudyGoalCreate,
    db: Session = Depends(get_db)

):
    new_goal = StudyGoal(**goal.dict())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return {
        "message": "study goal created"
    }




@router.get("/study-goals/{goal_id}")
def get_study_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    goal = db.query(StudyGoal).filter(
        StudyGoal.id == goal_id
        ).first()
    
    if goal is None:
        raise HTTPException(
            status_code=404, detail="Study goal not found")(
        )

    return goal


@router.put("/study-goals/{goal_id}")
def update_study_goal(
    goal_id: int,
    goal: StudyGoalUpdate,
    db: Session = Depends(get_db)
):
    update_goal = db.query(StudyGoal).filter(
        StudyGoal.id == goal_id
        ).first()
    
    if goal is None:
        raise HTTPException(
            status_code=404, 
            detail="Study goal not found"
        )
    update_goal.goal_title = goal.goal_title
    update_goal.target_hours = goal.target_hours
    update_goal.deadline = goal.deadline

    db.commit()
    db.refresh(update_goal)

    return {
        "message": "study goal updated"
    }

@router.delete("/study-goals/{goal_id}")
def delete_study_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    delete_goal = db.query(StudyGoal).filter(
        StudyGoal.id == goal_id
        ).first()
    
    if delete_goal is None:
        raise HTTPException(
            status_code=404, 
            detail="Study goal not found"
        )
    
    db.delete(delete_goal)
    db.commit()

    return {
        "message": "study goal deleted"
    }