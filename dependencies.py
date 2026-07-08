from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from auth import oauth2_scheme, decode_access_token


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    email = payload.get("sub")

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def admin_required(user=Depends(get_current_user)):
    if user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )
    return user


def agent_required(user=Depends(get_current_user)):
    if user.role != "Support Agent":
        raise HTTPException(
            status_code=403,
            detail="Support Agent only"
        )
    return user


def customer_required(user=Depends(get_current_user)):
    if user.role != "Customer":
        raise HTTPException(
            status_code=403,
            detail="Customer only"
        )
    return user