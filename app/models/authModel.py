from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from app.db.database import Base

class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    fin_kod = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    user_type = Column(Integer, nullable=False)  
    project_role = Column(Integer, nullable=False)
    approved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime)
    approved_at = Column(DateTime)
    # add not null for both created_at
    # 0 = teacher, 1 = phd, 2 = master