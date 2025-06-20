from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks # Added BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, crud, models
from ..core import security
from ..database import get_db
from ..core.config import settings
from ..utils.email_service import send_welcome_email # New import

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)): # Added background_tasks
    db_user_check = crud.user.get_user_by_email(db, email=user.email) # Renamed to avoid conflict
    if db_user_check:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = crud.user.create_user(db=db, user=user) # Renamed to created_user

    # Send welcome email in the background
    send_welcome_email(background_tasks, created_user.email, created_user.full_name or "New User")

    return created_user

@router.post("/login/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = security.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=schemas.Token)
def refresh_access_token(refresh_token_str: str = Depends(lambda token: token), db: Session = Depends(get_db)): # In a real app, pass token in body or header
    payload = security.decode_token(refresh_token_str)
    if not payload or payload.get("type") != "refresh": # Ensure it's a refresh token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    user = crud.user.get_user_by_email(db, email=email)
    if not user or not user.is_active: # Check if user exists and is active
        raise HTTPException(status_code=400, detail="User not found or inactive")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    # Optionally, issue a new refresh token as well for refresh token rotation
    # new_refresh_token = security.create_refresh_token(data={"sub": user.email})
    # return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": refresh_token_str} # Or return existing refresh token if not rotating
