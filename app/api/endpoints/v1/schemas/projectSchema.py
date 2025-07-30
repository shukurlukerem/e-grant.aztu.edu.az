from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    project_name: Optional[str]
    project_purpose: Optional[str]
    project_annotation: Optional[str]
    project_key_words: Optional[str]
    project_scientific_idea: Optional[str]
    project_structure: Optional[str]
    team_characterization: Optional[str]
    project_monitoring: Optional[str]
    project_assessment: Optional[str]
    project_requirements: Optional[str]
    project_deadline: Optional[datetime]
    collaborator_limit: Optional[int]
    max_smeta_amount: Optional[int] = 30000
    priotet: Optional[str]

class ProjectCreate(ProjectBase):
    fin_kod: str

class ProjectUpdate(ProjectBase):
    fin_kod: str

class ProjectOut(ProjectBase):
    project_code: int
    fin_kod: str
    approved: int
    submitted: bool
    submitted_at: Optional[datetime]

    class Config:
        orm_mode = True