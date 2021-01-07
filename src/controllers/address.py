from typing import List
from uuid import UUID

from models.pydanticmodels import AddressIn, AddressInPatch, AddressOut
from models.querymodels import AddressInQuery

from fastapi import APIRouter, Depends, HTTPException, status

from models.address import Address

from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)


@router.get("/", response_model=List[AddressOut], status_code=status.HTTP_200_OK)
def getAdresses(addressIn: AddressInQuery = Depends()):
    return Address().getAll(**addressIn.dict())


@router.get("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def getAddress(address_id: UUID):
    try:
        return Address().get(id=address_id)
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")


@router.post("/", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def addAddress(addressIn: AddressIn):
    
    return Address().insert(**addressIn.dict())


@router.patch("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def updateAddress(address_id: UUID, addressIn: AddressInPatch):
    try:
        return Address().update(address_id, **addressIn.dict(exclude_unset=True))
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")
    

@router.delete("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def deleteAddress(address_id: UUID):
    try:
        return Address().delete(address_id)
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")
