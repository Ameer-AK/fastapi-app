from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Address(BaseModel):
    __tablename__ = 'address'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey(
        "customer.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    street = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    last_updated = Column(DateTime, default=datetime.now,
                          onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    customer = relationship("Customer", back_populates="addresses")

    def as_json(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'street': self.street,
            'city': self.city,
            'country': self.country,
            'last_updated': self.last_updated,
            'created_at': self.created_at
        }


# audit = Table(
#     'audit', Base.metadata,
#     Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
#     Column('table', String(50)),
#     Column('item_id', UUID(as_uuid=True)),
#     Column('operation', Enum("INSERT", "UPDATE", "DELETE", name="operation_enum")),
#     Column('time', Time)
# )
