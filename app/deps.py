from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, UserRole
from .security import decode_token

def current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization[7:]
    data = decode_token(token)
    if not data.get("sub"):
        raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.phone == data["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(401, "User not found")
    return user

def require_role(*roles: UserRole):
    def check(user: User = Depends(current_user)) -> User:
        if user.role not in roles and user.role != UserRole.OWNER:
            raise HTTPException(403, "Forbidden")
        return user
    return check