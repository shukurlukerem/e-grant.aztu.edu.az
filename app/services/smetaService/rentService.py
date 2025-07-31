from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.smetaModels.rentModel import Rent
from app.models.smetaModels.smetaModel import Smeta
from app.api.endpoints.v1.schemas.smetaSchema.rentSchema import RentCreateSchema, RentUpdateSchema
from decimal import Decimal


async def create_rent(data: RentCreateSchema, db: AsyncSession):
    try:
        new_rent = Rent(**data.dict())

        result = await db.execute(select(Smeta).filter_by(project_code=str(data.project_code)))
        main_smeta = result.scalars().first()

        if not main_smeta:
            main_smeta = Smeta(project_code=str(data.project_code))
            db.add(main_smeta)

        if main_smeta.total_rent is None:
            main_smeta.total_rent = 0

        main_smeta.total_rent += data.total_amount

        db.add(new_rent)
        await db.commit()
        await db.refresh(new_rent)

        return new_rent
    except Exception as e:
        await db.rollback()
        raise e


async def get_all_rents(project_code: int, db: AsyncSession):
    result = await db.execute(select(Rent).filter_by(project_code=project_code))
    return result.scalars().all()


async def update_rent(project_code: int, data: RentUpdateSchema, db: AsyncSession):
    try:
        result = await db.execute(select(Rent).filter_by(project_code=project_code, id=data.id))
        rent = result.scalars().first()

        if not rent:
            return None

        old_total = rent.total_amount or 0

        for field, value in data.dict(exclude_unset=True).items():
            setattr(rent, field, value)

        if rent.unit_price and rent.quantity and rent.duration:
            rent.total_amount = rent.unit_price * rent.quantity * rent.duration

        new_total = rent.total_amount or 0

        result = await db.execute(select(Smeta).filter_by(project_code=str(project_code)))
        main_smeta = result.scalars().first()

        if not main_smeta:
            main_smeta = Smeta(project_code=str(project_code))
            db.add(main_smeta)

        if main_smeta.total_rent is None:
            main_smeta.total_rent = 0

        main_smeta.total_rent += Decimal(new_total - old_total)

        await db.commit()
        await db.refresh(rent)
        return rent
    except Exception as e:
        await db.rollback()
        raise e


async def delete_rent(project_code: int, rent_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Rent).filter_by(project_code=project_code, id=rent_id))
        rent = result.scalars().first()

        if not rent:
            return None

        result = await db.execute(select(Smeta).filter_by(project_code=str(project_code)))
        main_smeta = result.scalars().first()

        if not main_smeta:
            main_smeta = Smeta(project_code=project_code)
            db.add(main_smeta)

        if main_smeta.total_rent:
            main_smeta.total_rent -= rent.total_amount

        await db.delete(rent)
        await db.commit()

        return True
    except Exception as e:
        await db.rollback()
        raise e
