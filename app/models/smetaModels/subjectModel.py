from sqlalchemy import Column, Integer, String
from app.core.config import Base

class SubjectOfPurchase(Base):
    __tablename__ = "subjects_of_purchase"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    equipment_name = Column(String, nullable=False)
    unit_of_measure = Column(String, nullable=False)
    price = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)

    def subject_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'equipment_name': self.equipment_name,
            'unit_of_measure': self.unit_of_measure,
            'price': self.price,
            'quantity': self.quantity,
            'total_amount': self.total_amount
        }   