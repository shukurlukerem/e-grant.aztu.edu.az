from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.utils.jwt_required import token_required
from app.db.session import get_db
from app.api.endpoints.v1.schemas.smetaSchema.rentSchema import RentCreateSchema, RentUpdateSchema, RentResponseSchema
from app.services.smetaService.rentService import (
    create_rent,
    get_all_rents,
    update_rent,
    delete_rent,
)


router = APIRouter()


@router.post("/rent", response_model=RentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_rent_route(
    payload: RentCreateSchema,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2])),
):
    try:
        new_rent = await create_rent(payload, db)
        return new_rent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-rent-all-tables/{project_code}", response_model=List[RentResponseSchema])
async def get_all_rents_route(
    project_code: int,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 1, 2])),
):
    try:
        return await get_all_rents(project_code, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/edit-rent-table/{project_code}", response_model=RentResponseSchema)
async def update_rent_route(
    project_code: int,
    payload: RentUpdateSchema,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2])),
):
    try:
        updated = await update_rent(project_code, payload, db)
        if updated is None:
            raise HTTPException(status_code=404, detail="Rent record not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-rent-table/{project_code}/{id}", status_code=status.HTTP_200_OK)
async def delete_rent_route(
    project_code: int,
    id: int,
    db: AsyncSession = Depends(get_db),
    role: int = Depends(token_required([0, 2])),
):
    try:
        result = await delete_rent(project_code, id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Rent record not found")
        return {"message": "Rent record deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
