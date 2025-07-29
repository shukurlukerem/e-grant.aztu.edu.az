from sqlalchemy import Column, Integer, String, DateTime
from app.core.config import Base

class Prioritet(Base):
    __tablename__ = "prioritets"

    id = Column(Integer, primary_key=True, index=True)
    priority_name = Column(String, nullable=False)
    project_code = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
