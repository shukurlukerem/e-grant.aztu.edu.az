from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.smetaModels.smetaModel import Smeta
from app.models.projectModel import Project
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.api.endpoints.v1.schemas.smetaSchema.smetaSchema import SmetaCreate, SmetaUpdate

async def create_smeta(data: SmetaCreate, db: AsyncSession):
    try:
        new_smeta = Smeta(**data.dict())
        db.add(new_smeta)
        await db.commit()
        await db.refresh(new_smeta)
        return new_smeta
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def update_smeta_field(project_code: int, column: str, value: int, db: AsyncSession):
    try:
        result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
        smeta = result.scalars().first()
        if not smeta:
            raise HTTPException(status_code=404, detail="Smeta not found")
        if not hasattr(smeta, column):
            raise HTTPException(status_code=400, detail=f"Column '{column}' does not exist")
        setattr(smeta, column, value)
        await db.commit()
        await db.refresh(smeta)
        return smeta
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_main_smeta_by_project_code(project_code: int, db: AsyncSession):
    try:
        smeta_result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
        smeta = smeta_result.scalars().first()

        project_result = await db.execute(select(Project).where(Project.project_code == project_code))
        project = project_result.scalars().first()

        if not smeta or not project:
            raise HTTPException(status_code=404, detail="Project or Smeta not found")

        total_main_amount = sum([
            smeta.total_salary or 0,
            smeta.total_fee or 0,
            smeta.defense_fund or 0,
            smeta.total_equipment or 0,
            smeta.total_services or 0,
            smeta.total_rent or 0,
            smeta.other_expenses or 0
        ])
        return {
            "total_salary_smeta": smeta.total_salary,
            "total_tools_smeta": smeta.total_equipment,
            "total_services_smeta": smeta.total_services,
            "total_rent_smeta": smeta.total_rent,
            "total_other_smeta": smeta.other_expenses,
            "total_tax": smeta.total_fee,
            "total_defense_fund": smeta.defense_fund,
            "total_main_amount": total_main_amount,
            "max_amount_error": total_main_amount > project.max_smeta_amount
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_smeta(project_code: int, data: SmetaUpdate, db: AsyncSession):
    try:
        result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
        smeta = result.scalars().first()
        if not smeta:
            raise HTTPException(status_code=404, detail="Smeta not found")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(smeta, field, value)
        await db.commit()
        await db.refresh(smeta)
        return smeta
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def delete_smeta(project_code: int, db: AsyncSession):
    try:
        result = await db.execute(select(Smeta).where(Smeta.project_code == project_code))
        smeta = result.scalars().first()
        if not smeta:
            raise HTTPException(status_code=404, detail="Smeta not found")
        await db.delete(smeta)
        await db.commit()
        return {"message": "Smeta deleted"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
