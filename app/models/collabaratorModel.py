from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Collaborator(Base):  
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    fin_kod = Column(String, unique=True, index=True)
    approved = Column(Boolean, default=False, nullable=False)

    def collaborator_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'fin_code': self.fin_kod,  
            'approved': self.approved
        }
