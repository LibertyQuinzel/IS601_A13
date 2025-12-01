from sqlalchemy.orm import Session
from app.models import User, Calculation
from app.security import hash_password, verify_password
from app.schemas import UserCreate, CalculationCreate, CalculationUpdate


# ------------------------
# USER CRUD
# ------------------------

def get_user_by_email(db: Session, email: str):
    """Return a User or None for the given email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Return a User or None for the given id."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with a bcrypt-hashed password."""
    hashed = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user(db: Session, email: str, password: str):
    """Verify credentials; return the User on success or None on failure."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ------------------------
# CALCULATION CRUD
# ------------------------

def get_all_calculations(db: Session):
    return db.query(Calculation).all()


def get_calculation(db: Session, calc_id: int):
    return db.query(Calculation).filter(Calculation.id == calc_id).first()


def create_calculation(db: Session, calc: CalculationCreate):
    db_calc = Calculation(
        operation=calc.operation,
        number1=calc.number1,
        number2=calc.number2,
        result=calc.result,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


def update_calculation(db: Session, calc_id: int, updates: CalculationUpdate):
    calc = get_calculation(db, calc_id)
    if not calc:
        return None

    update_data = updates.model_dump(exclude_unset=True) if hasattr(updates, 'model_dump') else updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(calc, key, value)

    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc_id: int):
    calc = get_calculation(db, calc_id)
    if not calc:
        return False

    db.delete(calc)
    db.commit()
    return True
