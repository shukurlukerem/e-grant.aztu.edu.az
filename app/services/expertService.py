from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.expertModel import Expert
from app.models.projectModel import Project
from app.core.config import get_db
from app.api.endpoints.v1.schemas.expertSchema import ExpertCreate
from app.exceptions.exception import (
    handle_missing_field,
    handle_global_exception,
    handle_creation,
    handle_success,
    handle_specific_not_found,
)
from fastapi.templating import Jinja2Templates
from app.utils.email_util import send_email

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/email")

async def create_expert(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()

        required_fields = [
            'email', 'name', 'surname', 'father_name',
            'personal_id_serial_number', 'phone_number'
        ]

        for field in required_fields:
            if field not in data:
                return handle_missing_field(field)

        new_expert = Expert(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            father_name=data['father_name'],
            personal_id_serial_number=data['personal_id_serial_number'],
            work_place=data.get('work_place'),
            duty=data.get('duty'),
            scientific_degree=data.get('scientific_degree'),
            phone_number=data['phone_number']
        )

        db.add(new_expert)
        db.commit()
        db.refresh(new_expert)

        return handle_creation(new_expert, "Expert created successfully")

    except Exception as e:
        return handle_global_exception(str(e))


async def set_expert(request: Request, db: Session = Depends(get_db)):
    try:
        print("[DEBUG] Received request to set expert.")
        data = await request.json()
        print(f"[DEBUG] Request data: {data}")

        required_fields = [
            'email', 'project_code'
        ]

        for field in required_fields:
            if field not in data:
                return handle_missing_field(field)
            
        project = db.query(Project).filter_by(project_code=str(data['project_code'])).first()
        print(f"[DEBUG] Project found: {project}")

        if not project or project.submitted is False:
            return handle_success("Project not submitted.", status_code=409)

        project.expert = data['email']
        db.commit()

        subject = "Ekspert Təyinatı"
        recipient = data['email']
        html_content = templates.get_template("set_expert_email.html").render({"project": project})
        send_email(subject, recipient, html_content)

        print("[DEBUG] Expert set successfully.")
        return handle_success("Expert set successfully.")
    
    except Exception as e:
        print(f"[ERROR] set_expert failed: {e}")
        return handle_global_exception(str(e))

async def get_experts(db: Session = Depends(get_db)):
    try:
        print("[DEBUG] Fetching all experts from database...")
        experts = db.query(Expert).all()

        if not experts:
            return handle_specific_not_found("Expert not found.")

        experts_data = []
        for expert in experts:
            experts_data.append({
                "id": expert.id,
                "email": expert.email,
                "name": expert.name,
                "surname": expert.surname,
                "father_name": expert.father_name,
                "personal_id_serial_number": expert.personal_id_serial_number,
                "work_place": expert.work_place,
                "duty": expert.duty,
                "scientific_degree": expert.scientific_degree,
                "phone_number": expert.phone_number
            })

        return handle_success(experts_data, "Experts fetched successfully.")
    except Exception as e:
        print(f"[ERROR] get_experts failed: {e}")
        return handle_global_exception(str(e))