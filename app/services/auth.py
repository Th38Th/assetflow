from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, refresh_token

def create_user(user_in: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if user_in.email is not None:
        existing_user = existing_user or db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/email already taken"
        )
    hashed_pw = get_password_hash(user_in.password)
    user = User(username=user_in.username,
                email=user_in.email,
                hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(username: str, password:str, db: Session) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User \"{username}\" does not exist"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid password for user \"{username}\""
        )
    return user

def create_refresh_token_for_user(user: User) -> str:
    return create_refresh_token(user.username)

def create_access_token_for_user(user: User) -> str:
    return create_access_token(user.username)

def refresh_token_for_user(token: str) -> str:
    return refresh_token(token)