from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class DeliverablePriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DeliverableStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    BLOCKED = "blocked"

class Deliverable(Base):
    __tablename__ = "deliverables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(SAEnum(DeliverablePriority), default=DeliverablePriority.MEDIUM)
    status = Column(SAEnum(DeliverableStatus), default=DeliverableStatus.PENDING)
    estimated_effort_hours = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    project = relationship("Project", back_populates="deliverables")

    assigned_consultant_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    assigned_consultant = relationship("User", backref="assigned_deliverables")

    # dependency_id = Column(Integer, ForeignKey('deliverables.id'), nullable=True) # Simple one-to-one dependency
    # dependencies = relationship("Deliverable", remote_side=[id]) # For self-referential many-to-many, use association table

    attachments_urls = Column(Text, nullable=True) # Comma-separated URLs or JSON array string
