from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.finance import PaymentStatus

class ProjectBudgetBase(BaseModel):
    project_id: int
    estimated_budget: float
    total_payable: Optional[float] = 0.0
    paid_amount: Optional[float] = 0.0

class ProjectBudgetCreate(ProjectBudgetBase):
    pass

class ProjectBudgetUpdate(BaseModel):
    estimated_budget: Optional[float] = None
    total_payable: Optional[float] = None
    paid_amount: Optional[float] = None

class ProjectBudgetInDB(ProjectBudgetBase):
    id: int
    remaining_budget: float # Property
    variance: float       # Property
    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    project_id: int
    deliverable_id: Optional[int] = None
    consultant_id: Optional[int] = None
    amount: float
    currency: Optional[str] = "USD"
    due_date: Optional[datetime] = None
    status: Optional[PaymentStatus] = PaymentStatus.PENDING
    details: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    status: Optional[PaymentStatus] = None
    details: Optional[str] = None

class PaymentInDB(PaymentBase):
    id: int
    paid_date: Optional[datetime] = None
    class Config:
        orm_mode = True
