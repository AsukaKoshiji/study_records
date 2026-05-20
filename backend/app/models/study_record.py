from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date
from backend.app.database.database import Base


class StudyRecord(Base):
    __tablename__ = "study_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    study_time = Column(Integer, nullable=False)
    study_date = Column(Date, nullable=False)
    memo = Column(String, nullable=True)