from pydantic import BaseModel, Field
from datetime import date


class StudyGoalCreate(BaseModel):
    goal_title: str = Field(
        ...,
        min_length=1,  # 1文字以上でなければならない
        max_length=255,  # 255文字まで入力できる
    )

    target_hours: int = Field(
        ...,
        gt=0,  # 0より大きい数値でなければならない
    )

    deadline: date


class StudyGoalUpdate(BaseModel):
    goal_title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    target_hours: int = Field(
        ...,
        gt=0
    )

    deadline: date