from app.security import hash_password, verify_password
from app.schemas import UserCreate
import pytest
from app.security import _prepare_password_bytes

def test_password_hashing_and_verify():
    raw = "mypassword"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)

def test_user_schema_validation():
    data = {"username": "bob", "email": "wrongemail", "password": "pass123"}
    with pytest.raises(Exception):
        UserCreate(**data)


def test_prepare_password_bytes_type_error():
    with pytest.raises(TypeError):
        _prepare_password_bytes(123)  # non-string should raise


def test_hash_and_verify_short_and_long():
    short = "shortpw"
    long = "x" * 100
    hs = hash_password(short)
    assert hs != short
    assert verify_password(short, hs)

    hl = hash_password(long)
    assert verify_password(long, hl)
