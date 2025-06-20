from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional # Added Optional
import shutil
import os

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies.auth import get_current_active_user, get_consultant_user, get_admin_user

router = APIRouter()

CONTAINER_UPLOAD_DIR = "uploads/profile_pics"

@router.post("/profiles/me/upload-picture", response_model=schemas.ConsultantProfile)
async def upload_my_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_consultant_user)
):
    profile = crud.consultant_profile.get_consultant_profile(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Consultant profile not found for current user.")
    os.makedirs(CONTAINER_UPLOAD_DIR, exist_ok=True)
    filename = f"{current_user.id}_{file.filename.replace(' ', '_').replace('..', '')}"
    file_path = os.path.join(CONTAINER_UPLOAD_DIR, filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        file.file.close()
    profile.profile_picture_url = f"/static/profile_pics/{filename}"
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/profiles/", response_model=schemas.ConsultantProfile)
def create_new_consultant_profile(profile: schemas.ConsultantProfileCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    user_to_profile = crud.user.get_user(db, user_id=profile.user_id)
    if not user_to_profile: raise HTTPException(status_code=404, detail=f"User with id {profile.user_id} not found.")
    if user_to_profile.role != models.user.UserRole.CONSULTANT: raise HTTPException(status_code=400, detail=f"User {profile.user_id} is not a consultant.")
    if current_user.role == models.user.UserRole.CONSULTANT and current_user.id != profile.user_id: raise HTTPException(status_code=403, detail="Consultants can only create their own profile.")
    existing_profile = crud.consultant_profile.get_consultant_profile(db, user_id=profile.user_id)
    if existing_profile: raise HTTPException(status_code=400, detail=f"Consultant profile already exists for user {profile.user_id}. Use PUT to update.")
    created_profile = crud.consultant_profile.create_consultant_profile(db=db, profile=profile)
    if not created_profile: raise HTTPException(status_code=400, detail=f"Could not create profile. Ensure user {profile.user_id} is a consultant.")
    return created_profile

@router.get("/profiles/me", response_model=schemas.ConsultantProfile)
def read_my_consultant_profile(db: Session = Depends(get_db), current_user: models.User = Depends(get_consultant_user)):
    profile = crud.consultant_profile.get_consultant_profile(db, user_id=current_user.id)
    if profile is None: raise HTTPException(status_code=404, detail="Consultant profile not found for current user.")
    return profile

@router.put("/profiles/me", response_model=schemas.ConsultantProfile)
def update_my_consultant_profile(profile_update: schemas.ConsultantProfileUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_consultant_user)):
    db_profile = crud.consultant_profile.get_consultant_profile(db, user_id=current_user.id)
    if db_profile is None: raise HTTPException(status_code=404, detail="Consultant profile not found to update.")
    # Pydantic V2: model_dump(exclude_unset=True)
    update_data = profile_update.dict(exclude_unset=True)
    # Create a new schema instance for the update to ensure type validation
    return crud.consultant_profile.update_consultant_profile(db=db, db_profile=db_profile, profile_in=schemas.ConsultantProfileUpdate(**update_data))


@router.get("/profiles/{user_id}", response_model=schemas.ConsultantProfile, dependencies=[Depends(get_current_active_user)])
def read_consultant_profile_by_user_id(user_id: int, db: Session = Depends(get_db)):
    profile = crud.consultant_profile.get_consultant_profile(db, user_id=user_id)
    if profile is None: raise HTTPException(status_code=404, detail=f"Consultant profile not found for user {user_id}")
    return profile

@router.get("/profiles/", response_model=List[schemas.ConsultantProfile], dependencies=[Depends(get_current_active_user)])
def read_all_consultant_profiles(
    skip: int = 0, limit: int = 100, search: Optional[str] = None, # Added search
    db: Session = Depends(get_db)
):
    profiles = crud.consultant_profile.get_consultant_profiles(db, skip=skip, limit=limit, search=search) # Pass search
    return profiles
