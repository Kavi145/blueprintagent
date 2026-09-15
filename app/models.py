from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_request = Column(Text, nullable=False)
    plan_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())