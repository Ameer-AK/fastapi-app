from datetime import datetime
from uuid import uuid4

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Float,
                        Integer, String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customer'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, CheckConstraint('age>0'), CheckConstraint('age<100'))
    married = Column(Boolean, default=False)
    height = Column(Float)
    weight = Column(Float)
    last_updated = Column(DateTime, default=datetime.now,
                          onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    addresses = relationship(
        "Address", back_populates="customer", cascade="all, delete, delete-orphan")

    def as_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'age': self.age,
            'married': self.married,
            'height': self.height,
            'weight': self.weight,
            'last_updated': self.last_updated,
            'created_at': self.created_at,
            'addresses': [a.as_json() for a in self.addresses]
        }
