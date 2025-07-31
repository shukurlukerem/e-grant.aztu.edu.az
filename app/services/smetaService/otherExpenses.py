import logging
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.smetaModels.smetaModel import Smeta
from app.models.smetaModels.other_expensesModel import other_exp_model

logger = logging.getLogger(__name__)


async def create_other_exp(data, db: AsyncSession):
    try:
        new_other_exp = other_exp_model(**data.dict())
        project_code = str(data.project_code)

        result = await db.execute(select(Smeta).filter_by(project_code=project_code))
        main_smeta = result.scalars().first()

        if not main_smeta:
            main_smeta = Smeta(project_code=project_code)
            db.add(main_smeta)

        if main_smeta.other_expenses is None:
            main_smeta.other_expenses = 0
        main_smeta.other_expenses += data.total_amount

        db.add(new_other_exp)
        await db.commit()
        await db.refresh(new_other_exp)

        return {"message": "other_exp record created", "data": new_other_exp.others()}
    except Exception as e:
        logger.exception("Failed to create other_exp record")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_other_exps(project_code: int, db: AsyncSession):
    try:
        result = await db.execute(select(other_exp_model).filter_by(project_code=project_code))
        records = result.scalars().all()
        return [r.others() for r in records]
    except Exception as e:
        logger.exception("Failed to retrieve other_exp records")
        raise HTTPException(status_code=500, detail=str(e))


async def update_other_exp(id: int, data, db: AsyncSession):
    try:
        result = await db.execute(select(other_exp_model).filter_by(id=id))
        other_exp = result.scalars().first()
        if not other_exp:
            raise HTTPException(status_code=404, detail="other_exp record not found")

        old_total_amount = other_exp.total_amount or 0

        for key, value in data.dict(exclude_unset=True).items():
            setattr(other_exp, key, value)

        if "total_amount" in data.dict(exclude_unset=True):
            result = await db.execute(select(Smeta).filter_by(project_code=str(other_exp.project_code)))
            main_smeta = result.scalars().first()
            if not main_smeta:
                main_smeta = Smeta(project_code=other_exp.project_code)
                db.add(main_smeta)
            if main_smeta.other_expenses is None:
                main_smeta.other_expenses = 0
            main_smeta.other_expenses = Decimal(
                main_smeta.other_expenses - old_total_amount + other_exp.total_amount
            )

        await db.commit()
        await db.refresh(other_exp)
        return {"message": "other_exp record updated", "data": other_exp.others()}
    except Exception as e:
        logger.exception("Failed to update other_exp record")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_other_exp(project_code: int, id: int, db: AsyncSession):
    try:
        result = await db.execute(select(other_exp_model).filter_by(project_code=project_code, id=id))
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="other_exp record not found")

        result = await db.execute(select(Smeta).filter_by(project_code=str(project_code)))
        main_smeta = result.scalars().first()
        if not main_smeta:
            main_smeta = Smeta(project_code=project_code)
            db.add(main_smeta)

        if main_smeta.other_expenses:
            main_smeta.other_expenses -= record.total_amount

        await db.delete(record)
        await db.commit()
        return {"message": "other_exp record deleted"}
    except Exception as e:
        logger.exception("Error occurred in delete_other_exp")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
