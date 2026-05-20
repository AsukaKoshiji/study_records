from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal, Base
from backend.app.models.study_goal import StudyGoal
from backend.app.schemas.study_goal import StudyGoalCreate, StudyGoalUpdate

router = APIRouter()


# TODO: 将来的にテストを書きやすくするため、app/database/dependencies.py等へ移動を推奨
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/study-goals")
def get_study_goals(db: Session = Depends(get_db)):
    return db.query(StudyGoal).all()


@router.get("/study-goals/{goal_id}")
def get_study_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(StudyGoal).filter(StudyGoal.id == goal_id).first()
    
    if goal is None:
        raise HTTPException(status_code=404, detail="Study goal not found")  # 括弧のバグを修正

    return goal


@router.post("/study-goals", status_code=201)
def create_study_goal(goal: StudyGoalCreate, db: Session = Depends(get_db)):
    # dict() から model_dump() に変更
    new_goal = StudyGoal(**goal.model_dump())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return {"message": "study goal created"}


@router.put("/study-goals/{goal_id}")
def update_study_goal(goal_id: int, goal: StudyGoalUpdate, db: Session = Depends(get_db)):
    update_goal = db.query(StudyGoal).filter(StudyGoal.id == goal_id).first()
    
    # 判定対象を goal から update_goal に修正
    if update_goal is None:
        raise HTTPException(status_code=404, detail="Study goal not found")

    # フィールドの一括更新（ループで書くとスッキリします）
    for key, value in goal.model_dump(exclude_unset=True).items():
        setattr(update_goal, key, value)

    db.commit()
    db.refresh(update_goal)

    return {"message": "study goal updated"}


@router.delete("/study-goals/{goal_id}")
def delete_study_goal(goal_id: int, db: Session = Depends(get_db)):
    delete_goal = db.query(StudyGoal).filter(StudyGoal.id == goal_id).first()
    
    if delete_goal is None:
        raise HTTPException(status_code=404, detail="Study goal not found")
    
    db.delete(delete_goal)
    db.commit()

    return {"message": "study goal deleted"}