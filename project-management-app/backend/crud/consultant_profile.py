from sqlalchemy.orm import Session
from sqlalchemy import or_ # For search
from typing import Optional # For Optional search parameter
from .. import models, schemas

def get_consultant_profile(db: Session, user_id: int):
    return db.query(models.ConsultantProfile).filter(models.ConsultantProfile.user_id == user_id).first()

def get_consultant_profile_by_id(db: Session, profile_id: int):
    return db.query(models.ConsultantProfile).filter(models.ConsultantProfile.id == profile_id).first()

def get_consultant_profiles(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None): # Added search
    query = db.query(models.ConsultantProfile).join(models.User) # Join with User to search name
    if search:
        # Search in user's full_name, consultant profile skills (array contains), or category_tags
        search_term = f"%{search}%" # Prepare search term for ilike
        # For array columns, use .any() or .contains().
        # .any() requires the search term to be exactly one of the elements.
        # .contains([search]) would mean the array contains the single element 'search'.
        # If search is part of an element (e.g. 'React' in 'React Native'), .any(search_term_for_ilike) won't work directly with ilike.
        # A common way for partial match in array elements is to convert array to string or use specific DB functions.
        # For simplicity with standard SQLAlchemy, we'll use exact match for array elements here.
        # For ilike on array elements, a more complex query or DB-specific function might be needed.
        query = query.filter(
            or_(
                models.User.full_name.ilike(search_term),
                models.ConsultantProfile.skills.any(search),
                models.ConsultantProfile.category_tags.any(search)
            )
        )
    return query.offset(skip).limit(limit).all()


def create_consultant_profile(db: Session, profile: schemas.ConsultantProfileCreate):
    user = db.query(models.User).filter(models.User.id == profile.user_id).first()
    if not user or user.role != models.user.UserRole.CONSULTANT:
        return None
    db_profile = models.ConsultantProfile(**profile.dict()) # pydantic v2: model_dump()
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_consultant_profile(db: Session, db_profile: models.ConsultantProfile, profile_in: schemas.ConsultantProfileUpdate):
    # Pydantic V2 uses model_dump()
    update_data_dict = profile_in.dict(exclude_unset=True)

    # Handle profile_picture_url specifically if it's part of the update schema
    # and you don't want it to be None if not provided.
    # However, the current ConsultantProfileUpdate allows it to be set to None.
    # If profile_in.profile_picture_url is None and exclude_unset=True, it means client didn't send it, so it's not changed.
    # If client explicitly sends profile_picture_url = null/None, then it will be set to None.

    for key, value in update_data_dict.items():
        setattr(db_profile, key, value)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
