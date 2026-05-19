from pydantic import BaseModel, Field
from datetime import date
 


class StudyRecordCreate(BaseModel):
     title: str = Field(
          max_length=255,  #255文字まで入力できる
     )

     content: str

     study_time: int = Field(
          gt = 0.  #0より大きい数値でなければならない
     )

     study_date: date

     memo: str | None = Field(
          default=None,
          max_length=1000 #1000文字まで
     )    #入力しなくてもいいようにするため、Noneを許容する


class StudyRecordUpdate(BaseModel):
     title: str = Field(
          max_length=255,
     )

     content: str

     study_time: int = Field(
          gt=0
     )

     study_date: date

     memo: str | None = Field(
          default=None,
          max_length=1000
     )


     