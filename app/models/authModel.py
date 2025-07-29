from sqlalchemy import Column, Integer, String
from app.core.config import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    fin_kod = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    user_type = Column(Integer, nullable=False)  
    project_role = Column(Integer, nullable=False)
    # 0 = teacher, 1 = phd, 2 = master


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User fin_kod={self.fin_kod}>"

    def auth_details(self):
        return {
            'fin_kod': self.fin_kod,
            'user_type': self.user_type,
            'project_role': self.project_role
        }
