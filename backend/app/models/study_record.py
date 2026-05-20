from sqlalchemy import Column, Integer, String, Text, Date
from backend.app.database.database import Base


class StudyRecord(Base):
    __tablename__ = "study_records"

    # primary_key=True で自動インデックスされるため index=True は省略してOK
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    study_time = Column(Integer, nullable=False)  # 分単位 or 時間単位
    
    # 頻繁に検索（filter）で使われるカラムにインデックスを貼ると高速化する
    study_date = Column(Date, nullable=False, index=True)
    
    memo = Column(Text, nullable=True)

    # デバッグ時（printやログ）に中身が見やすくなるお守り
    def __repr__(self):
        return f"<StudyRecord id={self.id} title={self.title} date={self.study_date}>"