from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from .user import User as UserSchema # For embedding user info

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_budget: Optional[float] = None
    client_details: Optional[str] = None
    project_manager_id: Optional[int] = None
    custom_fields: Optional[dict] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    title: Optional[str] = None # All fields optional for update

class ProjectInDBBase(ProjectBase):
    id: int
    # project_manager: Optional[UserSchema] = None # For response model

    class Config:
        orm_mode = True

class Project(ProjectInDBBase):
    pass

# For responses that might include related objects
class ProjectWithDetails(Project):
    project_manager: Optional[UserSchema] = None
    # deliverables: List[Any] = [] # Define DeliverableSchema later
    # budget: Optional[Any] = None # Define BudgetSchema later
