import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date

from backend.app.database.database import Base
from backend.app.routers.study_record import get_progress
from backend.app.models.study_record import StudyRecord
from backend.app.models.study_goal import StudyGoal

# =========================================================
# テスト用SQLite in-memory DB
# =========================================================
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# =========================================================
# DB fixture
# =========================================================
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# =========================================================
# progressテスト：goalなし
# =========================================================
def test_progress_no_goal(db):
   
    db.add(StudyRecord(
        title="テスト", 
        content="テスト内容", 
        study_date=date(2026, 5, 20), 
        study_time=120
    ))
    db.commit()

    result = get_progress(db)

    assert result["total_study_time"] == 120
    assert result["target_hours"] == 0
    assert result["achievement_rate"] == 0.0


# =========================================================
# progressテスト：goalあり
# =========================================================
def test_progress_with_goal(db):
    
    db.add_all([
        StudyRecord(title="テスト1", content="内容1", study_date=date(2026, 5, 20), study_time=60),
        StudyRecord(title="テスト2", content="内容2", study_date=date(2026, 5, 20), study_time=40),
        StudyGoal(goal_title="基本情報", target_hours=10, deadline=date(2026, 6, 30)),
    ])
    db.commit()

    result = get_progress(db)
    assert result["total_study_time"] == 100
    assert result["target_hours"] == 10
    assert result["achievement_rate"] == 1000.0


# =========================================================
# progressテスト：goal = 0
# =========================================================
def test_progress_goal_zero(db):
    
    db.add_all([
        StudyRecord(title="テスト", content="内容", study_date=date(2026, 5, 20), study_time=100),
        StudyGoal(goal_title="目標0時間", target_hours=0, deadline=date(2026, 6, 30)),
    ])
    db.commit()

    result = get_progress(db)

    assert result["total_study_time"] == 100
    assert result["target_hours"] == 0
    assert result["achievement_rate"] == 0.0