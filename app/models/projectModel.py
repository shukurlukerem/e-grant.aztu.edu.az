from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.core.config import Base

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_code = Column(Integer, unique=True, nullable=False)
    fin_kod = Column(String, unique=True, nullable=False)
    project_name = Column(Text)
    project_purpose = Column(Text)
    project_annotation = Column(Text)
    project_key_words = Column(Text)
    project_scientific_idea = Column(Text)
    project_structure = Column(Text)
    team_characterization = Column(Text)
    project_monitoring = Column(Text)
    project_assessment = Column(Text)
    project_requirements = Column(Text)
    project_deadline = Column(DateTime)
    approved = Column(Integer, default=0)
    collaborator_limit = Column(Integer, nullable=False)
    max_smeta_amount = Column(Integer, nullable=False, default=30000)
    expert = Column(Text, default=None)
    priotet = Column(Text)
    submitted = Column(Boolean, default=False)
    submitted_at = Column(DateTime)

    def project_detail(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'fin_kod': self.fin_kod,
            'project_name': self.project_name,
            'project_purpose': self.project_purpose,
            'project_annotation': self.project_annotation,
            'project_key_words': self.project_key_words,
            'project_scientific_idea': self.project_scientific_idea,
            'project_structure': self.project_structure,
            'team_characterization': self.team_characterization,
            'project_monitoring': self.project_monitoring,
            'project_assessment': self.project_assessment,
            'project_requirements': self.project_requirements,
            'project_deadline': self.project_deadline,
            'approved': self.approved,
            'collaborator_limit': self.collaborator_limit,
            'max_smeta_amount': self.max_smeta_amount,
            'expert': self.expert,
            'priotet': self.priotet,
            'submitted': self.submitted,
            'submitted_at': self.submitted_at
        }
