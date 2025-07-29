from sqlalchemy import Column, Integer, String
from app.core.config import Base    

class Salary(Base):
    __tablename__ = "salary_smeta"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    fin_kod = Column(String, nullable=False)
    salary_per_month = Column(Integer, nullable=False)
    months = Column(Integer, nullable=False)
    total_salary = Column(Integer, nullable=False)

    def salary_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'fin_kod': self.fin_kod,
            'salary_per_month': self.salary_per_month,
            'months': self.months,
            'total_salary': self.total_salary
        }