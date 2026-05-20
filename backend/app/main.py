
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ルーターのインポート（database や Base は main では使わないので削除してOKです）
from backend.app.routers import study_record, study_goal

# アプリケーションの初期化（テーブル作成は conftest.py または本番のマイグレーションツールに任せます）
app = FastAPI()


# =========================================================
# 1. CORSの設定
# =========================================================
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 2. ルーターの登録
# =========================================================
app.include_router(
    study_record.router,
    prefix="/api/study-records",
    tags=["Study Records"],
)

app.include_router(
    study_goal.router,
    prefix="/api/study-goals",
    tags=["Study Goals"],
)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello FastAPI"}



