from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.database import engine, Base
from backend.app.routers import study_record, study_goal


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

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