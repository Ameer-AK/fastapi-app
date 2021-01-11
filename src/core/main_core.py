from pydanticmodels import CustomerIn, CustomerOut, DBCustomer, AddressIn, AddressInPatch, AddressOut, DBAddress
from coremetadata import customer, address, audit, engine

from typing import List
from uuid import UUID, uuid4
import json
import re
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.dialects import postgresql


@event.listens_for(engine, 'after_cursor_execute')
def log_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if context.isupdate or context.isinsert or context.isdelete:

        table = re.search(r"(?<=\bUPDATE\s)(\w+)",statement).group() if context.isupdate\
                else re.search(r"(?<=\bINTO\s)(\w+)",statement).group() if context.isinsert\
                else re.search(r"(?<=\bFROM\s)(\w+)",statement).group()

        item_id = parameters['id_1'] if context.isdelete else parameters['id']
        
        operation = "UPDATE" if context.isupdate else "INSERT" if context.isinsert else "DELETE"

        if table != 'audit':
            audit.insert().\
            values(id=uuid4(),\
                table=table,\
                item_id=item_id,\
                operation=operation,\
                time=datetime.now()\
                ).execute()


@app.get("/")
def root():
    return "Hello"


@app.get("/customers", response_model=List[CustomerOut])
def get_customers():
    customers =  select([customer]).execute().fetchall()
    result = []
    for c in customers:
        d = dict(c.items())
        d['addresses'] = jsonable_encoder(select([address]).\
            where(address.c.customer_id==c.id).\
            execute().fetchall())
        result.append(d)
    return result


@app.get("/customers/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: UUID):
    query = jsonable_encoder(select([customer])\
        .where(customer.c.id==customer_id)\
        .execute().first())
    
    if not query:
        raise HTTPException(404, "Customer not found")

    result = dict(query.items())
    result['addresses'] = jsonable_encoder(select([address]).\
            where(address.c.customer_id==customer_id).\
            execute().fetchall())

    return result


@app.post("/customers", response_model=CustomerOut)
def add_customer(customer_in: CustomerIn):
    newCustomer = DBCustomer(**customer_in.dict(), id=uuid4())
    customer.insert().values(**newCustomer.dict()).execute()

    return newCustomer


@app.patch("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: UUID, customer_in: CustomerIn):
    currentCustomer = jsonable_encoder(customer.select().where(customer.c.id==customer_id).execute().first())

    if not currentCustomer:
        raise HTTPException(404, "Customer not found")
    
    customer_in = DBCustomer(**customer_in.dict(exclude_unset=True), id=customer_id)
    currentCustomer.update(customer_in)

    currentCustomer = DBCustomer(**dict(currentCustomer))

    customer.update().\
        where(customer.c.id==customer_id).\
        values(**currentCustomer.dict()).\
        execute()

    result = currentCustomer.dict()
    result['addresses'] = jsonable_encoder(select([address]).\
            where(address.c.customer_id==customer_id).\
            execute().fetchall())

    return result


@app.delete("/customers/{customer_id}", response_model=DBCustomer)
def delete_customer(customer_id: UUID):
    currentCustomer = customer.select().where(customer.c.id==customer_id).execute().first()
    
    if not currentCustomer:
        raise HTTPException(404, "Customer not found")

    customer.delete().\
        where(customer.c.id==customer_id).\
        execute()
    
    return currentCustomer


@app.post("/addresses", response_model=AddressOut)
def add_address(address_in: AddressIn):
    newAddress = DBAddress(**address_in.dict(), id=uuid4())
    address.insert().values(**newAddress.dict()).execute()
    return newAddress


@app.patch("/adresses/{address_id}", response_model=AddressOut)
def update_address(address_id: UUID, address_in: AddressInPatch):
    currentAddress = jsonable_encoder(address.select().where(address.c.id==address_id).execute().first())

    if not currentAddress:
        raise HTTPException(404, "address not found")
    
    address_in = DBAddress(**address_in.dict(exclude_unset=True), id=address_id, customer_id=currentAddress["customer_id"])
    currentAddress.update(address_in)

    currentAddress = DBAddress(**dict(currentAddress))

    address.update().\
        where(address.c.id==address_id).\
        values(**currentAddress.dict()).\
        execute()

    return currentAddress


@app.delete("/addresses/{address_id}", response_model=AddressOut)
def delete_address(address_id: UUID):
    currentAddress = address.select().where(address.c.id==address_id).execute().first()
    
    if not currentAddress:
        raise HTTPException(404, "address not found")

    address.delete().\
        where(address.c.id==address_id).\
        execute()
    
    return currentAddress
