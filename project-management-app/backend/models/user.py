from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    CONSULTANT = "consultant"
    FINANCIAL_MANAGER = "financial_manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False) # For email verification
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.CONSULTANT)

    # Add relationships here later, e.g., projects, tasks, etc.
    # profile = relationship("ConsultantProfile", back_populates="user", uselist=False) # Example
