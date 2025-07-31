from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    father_name = Column(String, nullable=False)
    personal_id_serial_number = Column(String, unique=True, index=True)
    work_place = Column(String)
    duty = Column(String)
    scientific_degree = Column(String)
    phone_number = Column(String, nullable=False)