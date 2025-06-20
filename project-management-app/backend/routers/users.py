from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, crud, models
from ..database import get_db
from ..dependencies.auth import get_current_active_user, get_admin_user

router = APIRouter()

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

# New endpoint for user to update their own full_name
class UserSelfUpdate(schemas.BaseModel): # Inline schema for simplicity in subtask, ideally in schemas/user.py
    full_name: Optional[str] = None

@router.put("/me", response_model=schemas.User)
def update_user_me(user_in: UserSelfUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Convert UserSelfUpdate to UserUpdate for the CRUD operation
    # Ensure other fields are not accidentally wiped if UserUpdate allows more fields
    user_update_data = schemas.UserUpdate(full_name=user_in.full_name)
    return crud.user.update_user(db=db, db_user=current_user, user_in=user_update_data)


# Admin routes
@router.get("/", response_model=List[schemas.User], dependencies=[Depends(get_admin_user)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_admin_user)])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_admin_user)])
def update_existing_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Admin can update role, email etc.
    return crud.user.update_user(db=db, db_user=db_user, user_in=user)

@router.delete("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_admin_user)])
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Mark as inactive or truly delete, depending on policy. crud.user.delete_user performs a hard delete.
    # Consider changing to soft delete (is_active=False)
    return crud.user.delete_user(db=db, db_user=db_user)
