from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.v1.schemas.projectSchema import ProjectCreate, ProjectOut, ProjectUpdate
from app.db.session import get_db  
from typing import List
from app.services.projectService import (
    create_or_update_project, get_all_projects,
    get_project_by_code, get_project_by_fin_kod,
    update_project, delete_project
)


router = APIRouter()


@router.post("/save/project", response_model=ProjectOut)
async def save_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    result = await create_or_update_project(db, data)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Failed to save project."))
    return result["data"]


@router.get("/projects", response_model=List[ProjectOut])
async def fetch_projects(db: AsyncSession = Depends(get_db)):
    result = await get_all_projects(db)
    if not result.get("data"):
        raise HTTPException(status_code=404, detail="No projects found.")
    return result["data"]


@router.get("/project/{project_code}", response_model=ProjectOut)
async def fetch_project_by_code(project_code: int, db: AsyncSession = Depends(get_db)):
    result = await get_project_by_code(db, project_code)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Project not found."))
    return result["data"]


@router.get("/project/fin/{fin_kod}", response_model=ProjectOut)
async def fetch_project_by_fin(fin_kod: str, db: AsyncSession = Depends(get_db)):
    result = await get_project_by_fin_kod(db, fin_kod)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Project not found."))
    return result["data"]


@router.patch("/upd/project")
async def update_project_data(data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    result = await update_project(db, data)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Project not found to update."))
    return {"message": result["message"]}


@router.delete("/delete/project")
async def delete_project_data(fin_kod: str, db: AsyncSession = Depends(get_db)):
    result = await delete_project(db, fin_kod)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Project not found."))
    return {"message": result["message"]}
