import pytest
from fastapi.testclient import TestClient
from main import app
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_calc.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_calculation():
    response = client.post("/calculations/", json={
        "operation": "add",
        "number1": 5,
        "number2": 7,
        "result": 12
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 12
    assert "id" in data


def test_get_all_calculations():
    response = client.get("/calculations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_calculation():
    response = client.get("/calculations/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_calculation():
    response = client.put("/calculations/1", json={
        "operation": "subtract",
        "number1": 10,
        "number2": 3,
        "result": 7
    })
    assert response.status_code == 200
    assert response.json()["result"] == 7


def test_delete_calculation():
    response = client.delete("/calculations/1")
    assert response.status_code == 200

    response = client.get("/calculations/1")
    assert response.status_code == 404
