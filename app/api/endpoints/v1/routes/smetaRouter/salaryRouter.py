from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.endpoints.v1.schemas.smetaSchema.salarySchema import (
    SalaryCreateSchema,
    SalaryUpdateSchema,
    SalaryResponseSchema
)
from app.services.smetaService.salaryService import (
    add_salary,
    get_salary_smeta_by_project_code,
    get_all_salaries,
    update_salary,
    delete_salary
)
from app.utils.jwt_required import token_required
from app.db.session import get_db

router = APIRouter()


@router.post("/create-salary-table", response_model=SalaryResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_salary_route(
    payload: SalaryCreateSchema,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2]))
):
    try:
        salary = await add_salary(payload, db)
        return salary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/salary/smeta/{project_code}")
async def get_salary_smeta_by_project_code_route(
    project_code: int,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 1, 2]))
):
    try:
        result = await get_salary_smeta_by_project_code(project_code, db)
        if result is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-salaries-table", response_model=List[SalaryResponseSchema])
async def get_all_salaries_route(
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 1, 2]))
):
    try:
        return await get_all_salaries(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/edit-salary-table/{project_code}", response_model=SalaryResponseSchema)
async def update_salary_route(
    project_code: int,
    payload: SalaryUpdateSchema,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2]))
):
    try:
        updated = await update_salary(project_code, payload, db)
        if updated is None:
            raise HTTPException(status_code=404, detail="Salary record not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-salary/{project_code}")
async def delete_salary_route(
    project_code: int,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2]))
):
    try:
        result = await delete_salary(project_code, db)
        if not result:
            raise HTTPException(status_code=404, detail="Salary record not found")
        return {"message": "Salary record deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
