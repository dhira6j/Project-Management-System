from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# Importing UserRole from models to be used in schemas
from ..models.user import UserRole as UserModelRole

class UserRole(str, Enum):
    ADMIN = UserModelRole.ADMIN.value
    PROJECT_MANAGER = UserModelRole.PROJECT_MANAGER.value
    CONSULTANT = UserModelRole.CONSULTANT.value
    FINANCIAL_MANAGER = UserModelRole.FINANCIAL_MANAGER.value

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.CONSULTANT # Default role on creation

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole

    class Config:
        orm_mode = True # Changed from from_attributes = True for Pydantic v1 compatibility

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

# Schema for token data
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    # Add other relevant fields like user_id, roles if needed in token payload
