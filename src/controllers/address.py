from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from models.address import Address
from models.pydanticmodels import AddressIn, AddressInPatch, AddressOut
from models.querymodels import AddressInQuery
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)


@router.get("/", response_model=List[AddressOut], status_code=status.HTTP_200_OK)
def get(address_in: AddressInQuery = Depends()):
    return Address().get_all(**address_in.dict())


@router.get("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def get_address(address_id: UUID):
    try:
        return Address().get(id=address_id)
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")


@router.post("/", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def add_address(address_in: AddressIn):

    return Address().insert(**address_in.dict())


@router.patch("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def update_address(address_id: UUID, address_in: AddressInPatch):
    try:
        return Address().update(address_id, **address_in.dict(exclude_unset=True))
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")


@router.delete("/{address_id}", response_model=AddressOut, status_code=status.HTTP_200_OK)
def delete_address(address_id: UUID):
    try:
        return Address().delete(address_id)
    except NoResultFound:
        raise HTTPException(404, f"Address with id: {address_id} not found")
