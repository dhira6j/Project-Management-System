from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.deliverable import DeliverablePriority, DeliverableStatus # Import enums

class DeliverableBase(BaseModel):
    name: str
    description: Optional[str] = None
    priority: Optional[DeliverablePriority] = DeliverablePriority.MEDIUM
    status: Optional[DeliverableStatus] = DeliverableStatus.PENDING
    estimated_effort_hours: Optional[int] = None
    due_date: Optional[datetime] = None
    project_id: int
    assigned_consultant_id: Optional[int] = None
    attachments_urls: Optional[str] = None

class DeliverableCreate(DeliverableBase):
    pass

class DeliverableUpdate(DeliverableBase):
    name: Optional[str] = None # All fields optional for update
    project_id: Optional[int] = None # Usually not changed, but can be supported

class DeliverableInDBBase(DeliverableBase):
    id: int
    class Config:
        orm_mode = True

class Deliverable(DeliverableInDBBase):
    pass
