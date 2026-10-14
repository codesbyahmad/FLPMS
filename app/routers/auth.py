from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import LoginIn, TokenOut, UserOut, UserCreate
from ..security import verify_password, create_token, hash_password
from ..deps import current_user, require_role
from ..models import UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == payload.phone).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_token(user.phone, user.role.value)
    return TokenOut(access_token=token, user=UserOut.model_validate(user))

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

@router.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db),
                _: User = Depends(require_role(UserRole.OWNER))):
    if db.query(User).filter(User.phone == payload.phone).first():
        raise HTTPException(400, "Phone already exists")
    u = User(
        full_name=payload.full_name, phone=payload.phone, email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role, display_unit=payload.display_unit,
    )
    db.add(u); db.commit(); db.refresh(u)
    return u