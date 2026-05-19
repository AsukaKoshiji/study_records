from fastapi import APIRouter

router = APIRouter()


@router.get("/study-goals")
def get_study_goals():
    return {
        "message": "study goals"
    }