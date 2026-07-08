from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from auth import hash_password, verify_password, create_access_token
from database import get_db
from models import User
from schemas import UserRegister, UserLogin, Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    crud.create_user(db, new_user)

    return {
        "message": "User registered successfully"
    }


@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    # Check email
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )