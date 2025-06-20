from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import ARRAY # For skills array
from sqlalchemy.orm import relationship
from ..database import Base

class ConsultantProfile(Base):
    __tablename__ = "consultant_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False) # One-to-one with User

    skills = Column(ARRAY(String), nullable=True)
    experience_summary = Column(Text, nullable=True)
    organization = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    category_tags = Column(ARRAY(String), nullable=True)
    portfolio_url = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True) # New field

    user = relationship("User", backref="consultant_profile")
