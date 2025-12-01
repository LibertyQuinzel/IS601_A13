import pytest
from fastapi.testclient import TestClient
import os
from main import app
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_user.db"

# Ensure we start with a fresh sqlite file for the integration tests.
# Some CI runners or local runs may leave the file behind between runs,
# causing a pre-existing user to make the first registration fail.
db_file = "./test_user.db"
if os.path.exists(db_file):
    try:
        os.remove(db_file)
    except OSError:
        # If removal fails, continue; create_all will still work but tests
        # might fail. We don't want to crash the test import.
        pass

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


def test_user_register():
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer" or data.get("token_type") == "Bearer"


def test_user_duplicate_register():
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 400


def test_user_login_success():
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer" or data.get("token_type") == "Bearer"


def test_user_login_invalid_password():
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
