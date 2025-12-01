from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


# --------------
# USER
# --------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_min_length(cls, v: str):
        if not isinstance(v, str) or len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --------------
# CALCULATIONS
# --------------

class CalculationCreate(BaseModel):
    operation: str
    number1: float
    number2: float
    result: float | None = None


class CalculationRead(BaseModel):
    id: int
    operation: str
    number1: float
    number2: float
    result: float | None

    model_config = ConfigDict(from_attributes=True)


class CalculationUpdate(BaseModel):
    operation: str | None = None
    number1: float | None = None
    number2: float | None = None
    result: float | None = None

