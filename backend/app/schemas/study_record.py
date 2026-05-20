from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# Base Schema
# =========================================================

class StudyRecordBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    content: str = Field(
        ...,
        min_length=1,
    )

    study_time: int = Field(
        ...,
        ge=0,
    )

    study_date: date

    memo: Optional[str] = None


# =========================================================
# Create Schema
# =========================================================

class StudyRecordCreate(StudyRecordBase):
    pass


# =========================================================
# Update Schema
# =========================================================

class StudyRecordUpdate(StudyRecordBase):
    pass


# =========================================================
# Response Schema
# =========================================================

class StudyRecordResponse(StudyRecordBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )