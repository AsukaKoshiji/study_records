from pydantic import BaseModel
from datetime import date
 


class StudyRecordCreate(BaseModel):
     title: str
     content: str
     study_time: int
     study_date: date
     memo: str | None = None    #入力しなくてもいいようにするため、Noneを許容する


class StudyRecordUpdate(BaseModel):
     title: str
     content: str
     study_time: int
     study_date: date
     memo: str | None = None

     