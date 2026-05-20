from pydantic import BaseModel, Field, ConfigDict
from datetime import date


# ==========================================
# 共通ベーススキーマ（基本構造をここに集約）
# ==========================================
class StudyGoalBase(BaseModel):
    goal_title: str = Field(
        ...,
        min_length=1,   # 1文字以上
        max_length=255, # 255文字まで
        description="目標のタイトル"
    )

    target_hours: int = Field(
        ...,
        gt=0,  # 0より大きい数値（1以上）
        description="総目標学習時間（時間単位）"
    )

    deadline: date = Field(..., description="目標達成期限")


# ==========================================
# リクエスト（データ作成・更新）用
# ==========================================
class StudyGoalCreate(StudyGoalBase):
    """作成時はベースと同じでOK"""
    pass


class StudyGoalUpdate(StudyGoalBase):
    """更新時もベースと同じ（PUTでの全置換を想定）"""
    pass


# ==========================================
# レスポンス（APIがフロントに返すデータ）用【★新規追加】
# ==========================================
class StudyGoalResponse(StudyGoalBase):
    id: int  # DBで自動採番されたIDをフロントに返すために追加

    # SQLAlchemyのモデル（ORM）をPydanticが自動でパースするための設定（Pydantic v2用）
    model_config = ConfigDict(from_attributes=True)