from sqlalchemy import Column, Integer, String
from app.db.database import Base
class Rent(Base):
    __tablename__ = "rent_table"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    rent_area = Column(String, nullable=False)
    unit_of_measure = Column(String, nullable=False)
    unit_of_price = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)

    def rent(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'rent_area': self.rent_area,
            'unit_of_measure': self.unit_of_measure,
            'unit_of_price': self.unit_of_price,
            'quantity': self.quantity,
            'duration': self.duration,
            'total_amount': self.total_amount
        }