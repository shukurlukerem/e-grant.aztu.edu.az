from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.smetaService.otherExpenses import (
    create_other_exp,
    get_all_other_exps,
    update_other_exp,
    delete_other_exp
)
from app.utils.jwt_required import token_required
from app.api.endpoints.v1.schemas.smetaSchema.otherExpenses import OtherExpCreate, OtherExpUpdate
from app.db.session import get_db

router = APIRouter()


@router.post("/other_exp", status_code=201)
#@token_required([0, 2])
async def create_other_exp_endpoint(data: OtherExpCreate, db: Session = Depends(get_db)):
    return await create_other_exp(data, db)


@router.get("/get-other_exp-all-tables/{project_code}")
@token_required([0, 1, 2])
async def get_all_other_exps_endpoint(project_code: int, db: Session = Depends(get_db)):
    return await get_all_other_exps(project_code, db)


@router.patch("/edit-other_exp-table/{id}")
@token_required([0, 2])
async def update_other_exp_endpoint(id: int, data: OtherExpUpdate, db: Session = Depends(get_db)):
    return await update_other_exp(id, data, db)


@router.delete("/delete-other_exp-table/{project_code}/{id}")
@token_required([0, 2])
async def delete_other_exp_endpoint(project_code: int, id: int, db: Session = Depends(get_db)):
    return await delete_other_exp(project_code, id, db)
