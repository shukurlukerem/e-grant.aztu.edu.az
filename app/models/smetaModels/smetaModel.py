from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Smeta(Base):
    __tablename__ = "smeta"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    total_salary = Column(Integer, nullable=False)
    total_fee = Column(Integer, nullable=False)
    defense_fund = Column(Integer, nullable=False)
    total_equipment = Column(Integer, nullable=False)
    total_rent = Column(Integer, nullable=False)
    other_expenses = Column(Integer, nullable=False)

    def smeta_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'total_salary': self.total_salary,
            'total_fee': self.total_fee,
            'defense_fund': self.defense_fund,
            'total_equipment': self.total_equipment,
            'total_rent': self.total_rent,
            'other_expenses': self.other_expenses
        }
