from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Prioritet(Base):
    __tablename__ = "prioritets"

    id = Column(Integer, primary_key=True, index=True)
    prioritet_code = Column(String, nullable=False)
    prioritet_name = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)