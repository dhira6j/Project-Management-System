from pydantic import BaseModel
from typing import Optional, List

class ConsultantProfileBase(BaseModel):
    user_id: int
    skills: Optional[List[str]] = None
    experience_summary: Optional[str] = None
    organization: Optional[str] = None
    nationality: Optional[str] = None
    timezone: Optional[str] = None
    category_tags: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    profile_picture_url: Optional[str] = None # New field

class ConsultantProfileCreate(ConsultantProfileBase):
    pass

class ConsultantProfileUpdate(BaseModel):
    skills: Optional[List[str]] = None
    experience_summary: Optional[str] = None
    organization: Optional[str] = None
    nationality: Optional[str] = None
    timezone: Optional[str] = None
    category_tags: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    profile_picture_url: Optional[str] = None # New field for update too

class ConsultantProfileInDBBase(ConsultantProfileBase):
    id: int
    class Config:
        orm_mode = True

class ConsultantProfile(ConsultantProfileInDBBase):
    pass
