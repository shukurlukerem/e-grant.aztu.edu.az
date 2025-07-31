from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.endpoints.v1.schemas.projectSchema import ProjectCreate, ProjectOut, ProjectUpdate
from app.services.projectService import (
    
    create_or_update_project, get_all_projects,
    get_project_by_code, get_project_by_fin_kod,
    update_project, delete_project
)
from app.core.config import get_db
from typing import List

router = APIRouter()

@router.post("/save/project", response_model=ProjectOut)
def save_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = create_or_update_project(db, data)
    return project

@router.get("/projects", response_model=List[ProjectOut])
def fetch_projects(db: Session = Depends(get_db)):
    projects = get_all_projects(db)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found.")
    return projects

@router.get("/project/{project_code}", response_model=ProjectOut)
def fetch_project_by_code(project_code: int, db: Session = Depends(get_db)):
    project = get_project_by_code(db, project_code)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project

@router.get("/project/fin/{fin_kod}", response_model=ProjectOut)
def fetch_project_by_fin(fin_kod: str, db: Session = Depends(get_db)):
    project = get_project_by_fin_kod(db, fin_kod)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project

@router.patch("/upd/project")
def update_project_data(data: ProjectUpdate, db: Session = Depends(get_db)):
    updated = update_project(db, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found to update.")
    return {"message": "Project updated successfully."}

@router.delete("/delete/project")
def delete_project_data(fin_kod: str, db: Session = Depends(get_db)):
    result = delete_project(db, fin_kod)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"message": "Project deleted successfully."}
