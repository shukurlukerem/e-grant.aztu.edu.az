from sqlalchemy import Column, Integer, String
from app.db.database import Base

class other_exp_model(Base):
    __tablename__ = "other_expenses"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    expense_name = Column(String, nullable=False)
    unit_of_measure = Column(String, nullable=False)
    unit_of_price = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    total_ammount = Column(Integer, nullable=False)

    def others(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'expense_name': self.expense_name,
            'unit_of_measure': self.unit_of_measure,
            'unit_of_price': self.unit_of_price,
            'quantity': self.quantity,
            'duration': self.duration,
            'total_ammount': self.total_ammount
        }
