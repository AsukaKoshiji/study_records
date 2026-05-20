import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.database.database import Base, SessionLocal
from backend.app.routers.study_record import get_db

# 🛑 【超重要】ここが動かない原因のすべてでした。
# クラス名（StudyRecord, StudyGoal）まで個別に直接インポートを明示します。
# これにより、Base.metadata.create_all を呼んだ瞬間に、SQLite上に2つのテーブルが100%強制生成されます。
from backend.app.models.study_record import StudyRecord
from backend.app.models.study_goal import StudyGoal

# =========================================================
# 1. テスト用DB（SQLite in-memory）の設定
# =========================================================
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================================================
# 2. テーブル作成・削除（テスト全体で1回だけ実行）
# =========================================================
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    テスト全体の開始時に、登録されたすべてのモデルのテーブルを生成します。
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# =========================================================
# 3. DBセッション（テストケースごとに完全に独立）
# =========================================================
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


# =========================================================
# 4. FastAPI依存関係の上書き
# =========================================================
@pytest.fixture
def client(db_session):
    """
    Depends(get_db) をテスト用のクリーンなSQLiteセッションに差し替えます。
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()