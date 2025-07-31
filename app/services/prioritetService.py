from sqlalchemy.orm import Session
from app.models.prioritetModel import Prioritet
from app.exceptions.exception import (
    handle_missing_field,
    handle_global_exception,
    handle_creation,
    handle_conflict,
)
from fastapi.responses import JSONResponse
import datetime


def create_prioritet_service(data: dict, db: Session):
    try:
        prioritet_name = data.get('prioritet_name')
        prioritet_code = data.get('prioritet_code')

        if not prioritet_name or not prioritet_code:
            return handle_missing_field("prioritet_name or prioritet_code")

        existing = db.query(Prioritet).filter_by(prioritet_code=prioritet_code).first()
        if existing:
            return handle_conflict("Prioritet code already exists")

        new_prioritet = Prioritet(
            prioritet_name=prioritet_name,
            prioritet_code=prioritet_code,
            created_at=datetime.datetime.now()
        )

        db.add(new_prioritet)
        db.commit()
        db.refresh(new_prioritet)

        return handle_creation({
            "prioritet_name": new_prioritet.prioritet_name,
            "prioritet_code": new_prioritet.prioritet_code,
            "created_at": new_prioritet.created_at.isoformat()
        }, "Prioritet created successfully")

    except Exception as e:
        return handle_global_exception(str(e))


def get_prioritet_by_code_service(prioritet_code: str, db: Session):
    try:
        prioritet = db.query(Prioritet).filter(Prioritet.prioritet_code == prioritet_code).first()

        if not prioritet:
            return JSONResponse(
                status_code=404,
                content={"error": "Not Found", "message": f"Prioritet with code '{prioritet_code}' not found"}
            )

        return {
            "prioritet_name": prioritet.prioritet_name,
            "prioritet_code": prioritet.prioritet_code
        }

    except Exception as e:
        return handle_global_exception(str(e))
