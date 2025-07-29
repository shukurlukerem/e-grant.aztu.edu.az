from sqlalchemy import Column, Integer, Text, DateTime, LargeBinary
from app.core.config import Base  
from datetime import datetime
import base64

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    surname = Column(Text)
    father_name = Column(Text)
    fin_kod = Column(Text, unique=True, nullable=False)
    image = Column(LargeBinary)
    born_place = Column(Text)
    living_location = Column(Text)
    home_phone = Column(Text, unique=True)
    personal_mobile_number = Column(Text, unique=True)
    personal_email = Column(Text, unique=True)
    citizenship = Column(Text)
    personal_id_number = Column(Text)
    sex = Column(Text)
    work_place = Column(Text)
    department = Column(Text)
    duty = Column(Text)
    main_education = Column(Text)
    additonal_education = Column(Text)
    scientific_degree = Column(Text)
    scientific_date = Column(DateTime)
    scientific_name = Column(Text)
    scientific_name_date = Column(DateTime)
    work_location = Column(Text)
    work_phone = Column(Text, unique=True)
    work_email = Column(Text, unique=True)
    profile_completed = Column(Integer, nullable=False)
    born_date = Column(DateTime)

    def user_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "father_name": self.father_name,
            "fin_kod": self.fin_kod,
            "image": base64.b64encode(self.image).decode('utf-8') if self.image else None,
            "born_place": self.born_place,
            "living_location": self.living_location,
            "home_phone": self.home_phone,
            "personal_mobile_number": self.personal_mobile_number,
            "personal_email": self.personal_email,
            "citizenship": self.citizenship,
            "personal_id_number": self.personal_id_number,
            "sex": self.sex,
            "work_place": self.work_place,
            "department": self.department,
            "duty": self.duty,
            "main_education": self.main_education,
            "additonal_education": self.additonal_education,
            "scientific_degree": self.scientific_degree,
            "scientific_date": self.scientific_date,
            "scientific_name": self.scientific_name,
            "scientific_name_date": self.scientific_name_date,
            "work_location": self.work_location,
            "work_phone": self.work_phone,
            "work_email": self.work_email,
            "profile_completed": self.profile_completed,
            "born_date": self.born_date
        }

    def get_user_image(self):
        return {
            "image": base64.b64encode(self.image).decode('utf-8') if self.image else None
        }
