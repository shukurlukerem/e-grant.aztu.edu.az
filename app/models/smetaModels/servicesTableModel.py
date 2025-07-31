from sqlalchemy import Column, Integer, String
from app.db.database import Base

class ServicesOfPurchase(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(Integer, nullable=False)
    service_name = Column(String, nullable=False)
    unit_of_measure = Column(String, nullable=False)
    price = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)

    def service(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'service_name': self.service_name,
            'unit_of_measure': self.unit_of_measure,
            'price': self.price,
            'quantity': self.quantity,
            'total_amount': self.total_amount
        }
