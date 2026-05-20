import pytest


# =========================================================
# GET /study-records
# =========================================================

def test_get_study_records_empty(client):
    """
    データが存在しない場合、
    空配列が返ることを確認する。
    """

    response = client.get("/api/study-records")

    assert response.status_code == 200
    assert response.json() == []


# =========================================================
# POST /study-records
# =========================================================

def test_create_study_record(client):
    """
    学習記録を新規作成できることを確認する。
    """

    payload = {
        "title": "FastAPI Study",
        "content": "FastAPIを学習した",
        "study_time": 60,
        "study_date": "2026-05-20",
        "memo": "REST API",
    }

    response = client.post(
        "/api/study-records",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "FastAPI Study"
    assert data["study_time"] == 60
    assert "id" in data


# =========================================================
# GET after POST
# =========================================================

def test_get_study_records_after_create(client):
    """
    作成後に一覧取得すると、
    登録データが返ることを確認する。
    """

    payload = {
        "title": "SQLAlchemy Study",
        "content": "ORMの学習",
        "study_time": 90,
        "study_date": "2026-05-20",
        "memo": "session確認",
    }

    client.post(
        "/api/study-records",
        json=payload,
    )

    response = client.get("/api/study-records")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "SQLAlchemy Study"
    assert data[0]["study_time"] == 90


# =========================================================
# Validation Test
# =========================================================

def test_create_study_record_validation_error(client):
    """
    不正データの場合、
    バリデーションエラーになることを確認する。
    """

    payload = {
        "title": "",
        "content": "",
        "study_time": -1,
        "study_date": "2026-05-20",
    }

    response = client.post(
        "/api/study-records",
        json=payload,
    )

    assert response.status_code == 422


# =========================================================
# GET /study-records/{id}
# =========================================================

def test_get_study_record_by_id(client):
    """
    ID指定で学習記録を取得できることを確認する。
    """

    payload = {
        "title": "Python Study",
        "content": "pytest学習",
        "study_time": 120,
        "study_date": "2026-05-20",
        "memo": "fixture確認",
    }

    create_response = client.post(
        "/api/study-records",
        json=payload,
    )

    assert create_response.status_code == 201

    created_data = create_response.json()

    record_id = created_data["id"]

    response = client.get(
        f"/api/study-records/{record_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == record_id
    assert data["title"] == "Python Study"
    assert data["study_time"] == 120