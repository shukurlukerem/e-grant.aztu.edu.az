from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.utils.jwt_required import token_required
from app.services.smetaService.subjectService import (
    add_subject,
    get_subjects,
    update_subject,
    delete_subject
)
from fastapi.responses import JSONResponse
from app.api.endpoints.v1.schemas.smetaSchema.subjectSchema import SubjectCreate, SubjectUpdate

router = APIRouter()

@router.post("/add-subject")
@token_required([0, 2])
async def add_subject_route(
    data: SubjectCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await add_subject(data.dict(), db)
    return JSONResponse(status_code=201, content=result)


@router.get("/subject/smeta/{project_code}")
@token_required([0, 1, 2])
async def get_subjects_route(
    project_code: int,
    db: AsyncSession = Depends(get_db)
):
    result = await get_subjects(project_code, db)
    return JSONResponse(status_code=200, content={"message": "Smeta fetched successfully.", "data": result})


@router.patch("/update-subject/{project_code}")
@token_required([0, 2])
async def update_subject_route(
    project_code: int,
    data: SubjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await update_subject(project_code, data.dict(exclude_unset=True), db)
    return JSONResponse(status_code=200, content=result)


@router.delete("/delete/smeta/subject/{project_code}")
@token_required([0, 2])
async def delete_subject_route(
    project_code: int,
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await delete_subject(project_code, id, db)
    return JSONResponse(status_code=200, content=result)