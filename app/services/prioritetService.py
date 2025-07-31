from sqlalchemy.orm import Session
from app.models.prioritetModel import Prioritet
from fastapi.responses import JSONResponse
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from app.db.session import get_db

async def create_prioritet_service(data: dict, db: AsyncSession = Depends(get_db)):
    try:
        prioritet_name = data.get('prioritet_name')
        prioritet_code = data.get('prioritet_code')

        if not prioritet_name or not prioritet_code:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Missing field: 'prioritet_name' or 'prioritet_code'"}
            )

        result = await db.execute(select(Prioritet).where(Prioritet.project_code == dict.prioritet_code))
        existing = result.scalar_one_or_none()

        if existing:
            return JSONResponse(
                status_code=409,
                content={"success": False, "message": "Prioritet code already exists"}
            )

        new_prioritet = Prioritet(
            prioritet_name=prioritet_name,
            prioritet_code=prioritet_code,
            created_at=datetime.datetime.now()
        )

        db.add(new_prioritet)
        db.commit()
        db.refresh(new_prioritet)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Prioritet created successfully",
                "data": {
                    "prioritet_name": new_prioritet.prioritet_name,
                    "prioritet_code": new_prioritet.prioritet_code,
                    "created_at": new_prioritet.created_at.isoformat()
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error", "error": str(e)}
        )


async def get_prioritet_by_code_service(prioritet_code: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Prioritet))
        prioritet = result.scalar_one_or_none()

        if not prioritet:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": f"Prioritet with code '{prioritet_code}' not found"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "prioritet_name": prioritet.prioritet_name,
                    "prioritet_code": prioritet.prioritet_code
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error", "error": str(e)}
        )
