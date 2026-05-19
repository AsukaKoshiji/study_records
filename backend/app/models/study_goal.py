from sqlalchemy import Column, Integer, String, Date
from app.database.database import Base


class StudyGoal(Base):
    __tablename__ = "study_goals"

    id = Column(Integer, primary_key=True, index=True)
    goal_title = Column(String(255), nullable=False)
    target_hours = Column(Integer, nullable=False)
    deadline = Column(Date, nullable=False)
