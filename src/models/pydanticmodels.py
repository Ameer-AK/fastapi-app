from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import Query
from pydantic import BaseModel, Field


class AddressIn(BaseModel):
    customer_id: UUID
    street: Optional[str] = None
    city: str
    country: str


class AddressInPatch(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class AddressOutEmbedded(BaseModel):
    id: UUID
    street: Optional[str] = None
    city: str
    country: str


class AddressOut(BaseModel):
    id: UUID
    customer_id: UUID
    street: Optional[str] = None
    city: str
    country: str


class DBAddress(AddressOut):
    id: UUID = uuid4()
    customer_id: UUID
    street: Optional[str] = None
    city: str
    country: str


class CustomerIn(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int = Field(..., gt=0, lt=100)
    married: bool = False
    height: float
    weight: float


class CustomerInPatch(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, lt=100)
    married: Optional[bool] = None
    height: Optional[float] = None
    weight: Optional[float] = None


class DBCustomer(BaseModel):
    id: UUID = uuid4()
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int = Field(..., gt=0, lt=100)
    married: bool = False
    height: float
    weight: float


class CustomerOut(BaseModel):
    id: UUID
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int = Field(..., gt=0, lt=100)
    married: bool
    height: float
    weight: float
    addresses: Optional[List[AddressOutEmbedded]] = None
