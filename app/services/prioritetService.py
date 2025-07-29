from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.prioritetModel import Prioritet
from app.core.config import get_db
from app.exceptions.exception import (
    handle_missing_field,
    handle_global_exception,
    handle_creation,
)
import datetime

router = APIRouter()

async def create_prioritet(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        prioritet_name = data.get('prioritet_name')
        prioritet_code = data.get('prioritet_code')

        if not prioritet_name or not prioritet_code:
            return handle_missing_field("prioritet_name or prioritet_code")
        
        new_prioritet = Prioritet(
            prioritet_name=prioritet_name,
            prioritet_code=prioritet_code,
            created_at=datetime.datetime.now()
        )

        db.add(new_prioritet)
        db.commit()
        db.refresh(new_prioritet)

        return handle_creation(new_prioritet, "Prioritet created successfully")
    
    except Exception as e:
        return handle_global_exception(str(e))


async def get_prioritet_by_code(prioritet_code: str, db: Session = Depends(get_db)):
    try:
        prioritet = db.query(Prioritet).filter(Prioritet.prioritet_code == prioritet_code).first()

        if not prioritet:
            return handle_missing_field("prioritet_code")

        return {
            "prioritet_name": prioritet.prioritet_name,
            "prioritet_code": prioritet.prioritet_code
        }

    except Exception as e:
        return handle_global_exception(str(e))