from sqlalchemy import Column, Integer, String, Text, Date
from app.database.database import Base


class StudyRecord(Base):
    __tablename__ = "study_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    study_time = Column(Integer, nullable=False)
    study_date = Column(Date, nullable=False)
    memo = Column(Text, nullable=True)
    