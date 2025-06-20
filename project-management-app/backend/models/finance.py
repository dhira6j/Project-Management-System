from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class ProjectBudget(Base):
    __tablename__ = "project_budgets"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), unique=True, nullable=False) # One-to-one with Project
    estimated_budget = Column(Float, nullable=False, default=0.0)
    total_payable = Column(Float, nullable=False, default=0.0) # Sum of committed payments
    paid_amount = Column(Float, nullable=False, default=0.0)

    project = relationship("Project", backref="budget") # Use backref for one-to-one

    @property
    def remaining_budget(self):
        return self.estimated_budget - self.paid_amount

    @property
    def variance(self): # Simple variance against estimated
        return self.estimated_budget - self.total_payable


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'), nullable=True) # Optional, payment might be general
    consultant_id = Column(Integer, ForeignKey('users.id'), nullable=True) # Who is being paid

    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    due_date = Column(DateTime, nullable=True)
    paid_date = Column(DateTime, nullable=True)
    status = Column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING)
    details = Column(Text, nullable=True) # e.g., invoice number, notes

    project = relationship("Project", backref="payments")
    deliverable = relationship("Deliverable", backref="payments")
    consultant = relationship("User", backref="received_payments")
