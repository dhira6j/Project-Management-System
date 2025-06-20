from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User # For ForeignKey

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    estimated_budget = Column(Float, nullable=True)
    client_details = Column(Text, nullable=True) # Could be JSON if structured

    project_manager_id = Column(Integer, ForeignKey('users.id'), nullable=True) # A project might not have a PM initially
    project_manager = relationship("User", backref="managed_projects")

    custom_fields = Column(JSON, nullable=True) # For flexibility

    deliverables = relationship("Deliverable", back_populates="project", cascade="all, delete-orphan")
    # budget = relationship("ProjectBudget", back_populates="project", uselist=False, cascade="all, delete-orphan") # Added later
