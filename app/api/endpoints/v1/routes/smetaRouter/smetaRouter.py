# router/router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.utils.jwt_required import token_required
from app.api.endpoints.v1.schemas.smetaSchema.smetaSchema import (
    SmetaCreate,
    SmetaUpdate,
    SmetaFieldUpdate
)



from app.services.smetaService.smetaService import (
    create_smeta,
    update_smeta_field,
    get_main_smeta_by_project_code,
    update_smeta,
    delete_smeta,
)

router = APIRouter()

@router.post("/create-smeta")
@token_required([0, 2])
async def create_smeta_route(
    data: SmetaCreate,
    db: AsyncSession = Depends(get_db)
):
    smeta = await create_smeta(data, db)
    return JSONResponse(status_code=201, content={"message": "Smeta created", "data": smeta.serialize()})


@router.patch("/update-smeta-field/{project_code}")
@token_required([0, 2])
async def update_smeta_field_route(
    project_code: int,
    data: SmetaFieldUpdate,
    db: AsyncSession = Depends(get_db)
):
    smeta = await update_smeta_field(project_code, data.column, data.value, db)
    return JSONResponse(status_code=200, content={"message": f"'{data.column}' updated successfully", "data": smeta.serialize()})


@router.get("/main-smeta/{project_code}")
@token_required([0, 1, 2])
async def get_main_smeta_by_project_code_route(
    project_code: int,
    db: AsyncSession = Depends(get_db)
):
    main_smeta_data = await get_main_smeta_by_project_code(project_code, db)
    return JSONResponse(status_code=200, content={"message": "Smeta fetched successfully.", "data": main_smeta_data})


@router.patch("/edit-smeta/{project_code}")
@token_required([0, 2])
async def update_smeta_route(
    project_code: int,
    data: SmetaUpdate,
    db: AsyncSession = Depends(get_db)
):
    smeta = await update_smeta(project_code, data, db)
    return JSONResponse(status_code=200, content={"message": "Smeta updated", "data": smeta.serialize()})


@router.delete("/delete-smeta/{project_code}")
@token_required([0, 2])
async def delete_smeta_route(
    project_code: int,
    db: AsyncSession = Depends(get_db)
):
    result = await delete_smeta(project_code, db)
    return JSONResponse(status_code=200, content=result)
