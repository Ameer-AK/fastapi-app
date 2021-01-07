from dataclasses import dataclass
from typing import Optional, Dict, List
from fastapi import Query
from uuid import UUID
from pydantic import StrictStr

@dataclass
class BaseQuery:
    def dict(self):
        return {k:v for k, v in self.__dict__.items() if not v is None}

@dataclass
class CustomerInQuery(BaseQuery):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Query(None, gt=0, lt=100)
    married: Optional[bool] = None
    height: Optional[float] = None
    weight: Optional[float] = None

@dataclass
class AddressInQuery(BaseQuery):
    customer_id: Optional[UUID] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None