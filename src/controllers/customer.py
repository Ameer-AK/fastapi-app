from models.customer import Customer
# audit

from models.pydanticmodels import CustomerIn, CustomerInPatch, CustomerOut
from models.querymodels import CustomerInQuery

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.get("/", response_model=List[CustomerOut], status_code=status.HTTP_200_OK)
def getCustomers(customerIn: CustomerInQuery = Depends()):
    return Customer().getAll(**customerIn.dict())

@router.get("/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
def getCustomer(customer_id: UUID):
    try:
        return Customer().get(id=customer_id)
    except NoResultFound:
        raise HTTPException(404, f"Customer with id: {customer_id} not found")


@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def addCustomer(customerIn: CustomerIn):

    return Customer().insert(**customerIn.dict())


@router.patch("/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
def updateCustomer(customer_id: UUID, customerIn: CustomerInPatch):
    try:
        return Customer().update(customer_id, **customerIn.dict(exclude_unset=True))
    except NoResultFound:
        raise HTTPException(404, f"Customer with id: {customer_id} not found")
    

@router.delete("/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
def deleteCustomer(customer_id: UUID):
    try:
        return Customer().delete(customer_id)
    except NoResultFound:
        raise HTTPException(404, f"Customer with id: {customer_id} not found")
