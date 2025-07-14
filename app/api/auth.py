from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from datetime import datetime, timezone
from app.schemas.user import UserCreate, TokenWithRefresh
from app.schemas.message import Messsage
from app.kafka.producer import send_event
from app.core.security import oauth2_scheme, blacklist_token
from app.services.auth import authenticate_user, create_user, create_access_token_for_user, create_refresh_token_for_user, refresh_token_for_user

router = APIRouter()

@router.post("/signup", response_model=TokenWithRefresh, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(user, db)
    token = create_access_token_for_user(user)
    await send_event("user.signup", {
        "time": datetime.now(timezone.utc).isoformat(),
        "username": user.username,
        "email": user.email
    })
    return {"access_token": token, "token_type": "Bearer"}

@router.post("/login", response_model=TokenWithRefresh, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_user = authenticate_user(form_data.username, form_data.password, db)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token_for_user(auth_user)
    refresh_token = create_refresh_token_for_user(auth_user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

@router.post("/refresh", response_model=TokenWithRefresh, status_code=status.HTTP_202_ACCEPTED)
def refresh_token(refresh_token: str = Body(...)):
    return refresh_token_for_user(refresh_token)

@router.post("/logout", response_model=Messsage, status_code=status.HTTP_200_OK)
def signout_user(token: str = Depends(oauth2_scheme)):
    blacklist_token(token)
    return {"message": "Successfully logged out"}