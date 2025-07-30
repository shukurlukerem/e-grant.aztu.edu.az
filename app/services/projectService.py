from sqlalchemy.orm import Session
from app.models.projectModel import Project
from app.api.endpoints.v1.schemas import ProjectCreate, ProjectUpdate
from datetime import datetime
import random


def generate_unique_project_code(db: Session) -> int:
    while True:
        code = random.randint(10000000, 99999999)
        if not db.query(Project).filter_by(project_code=code).first():
            return code

def create_or_update_project(db: Session, data: ProjectCreate):
    project = db.query(Project).filter_by(fin_kod=data.fin_kod).first()
    if not project:
        project = Project(
            fin_kod=data.fin_kod,
            project_code=generate_unique_project_code(db)
        )
        db.add(project)

    for field, value in data.dict().items():
        if hasattr(project, field) and value is not None:
            setattr(project, field, value)

    required_fields = [
        'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure',
        'team_characterization', 'project_monitoring', 'project_requirements',
        'project_deadline', 'collaborator_limit', 'max_smeta_amount', 'priotet'
    ]

    all_fields_filled = all(getattr(project, field) for field in required_fields)
    project.approved = 1 if all_fields_filled else 0

    db.commit()
    db.refresh(project)
    return project

def get_all_projects(db: Session):
    return db.query(Project).all()

def get_project_by_code(db: Session, project_code: int):
    return db.query(Project).filter_by(project_code=project_code).first()

def get_project_by_fin_kod(db: Session, fin_kod: str):
    return db.query(Project).filter_by(fin_kod=fin_kod).first()

def update_project(db: Session, data: ProjectUpdate):
    project = db.query(Project).filter_by(fin_kod=data.fin_kod).first()
    if not project:
        return None
    for field, value in data.dict().items():
        if hasattr(project, field) and value is not None:
            setattr(project, field, value)
    db.commit()
    return project

def delete_project(db: Session, fin_kod: str):
    project = db.query(Project).filter_by(fin_kod=fin_kod).first()
    if not project:
        return None
    db.delete(project)
    db.commit()
    return True

