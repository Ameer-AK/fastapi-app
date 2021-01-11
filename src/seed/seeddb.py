import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from os import environ

from models.pydanticmodels import DBCustomer, DBAddress
from coremetadata import address, customer
from uuid import UUID, uuid4
from random import randint


with open('seed/lists/names.txt') as f:
    first_names = [l.strip() for l in f.readlines()]

with open('seed/lists/lastnames.txt') as f:
    last_names = [l.strip() for l in f.readlines()]

with open('seed/lists/streets.txt') as f:
    streets = [l.strip() for l in f.readlines()]
    
with open('seed/lists/cities.txt') as f:
    cities = [l.strip() for l in f.readlines()]

with open('seed/lists/countries.txt') as f:
    countries = [l.strip() for l in f.readlines()]


from sqlalchemy import *

db_username = environ.get('DB_USERNAME')
db_password = environ.get('DB_PASSWORD')
db_hostname = environ.get('DB_HOSTNAME')
db_name = environ.get('DB_NAME')

engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_hostname}/{db_name}')

conn = engine.connect()
conn.execute(customer.delete())
conn.execute(address.delete())

for i in range(100):
    index1 = randint(0, 49)
    index2 = randint(0, 49)
    
    cId = str(uuid4())
    aId1 = str(uuid4())
    aId2 = str(uuid4())

    customer_in = DBCustomer(
        id=cId,
        first_name= first_names[index1],
        middle_name= None,
        last_name= last_names[index2],
        age= randint(1, 99),
        married= randint(0,1),
        height= randint(100, 200),
        weight= randint(60, 150)
    )

    address_in1 = DBAddress(
        id = aId1,
        customer_id = cId,
        street=streets[index1],
        city=cities[index1],
        country=countries[index2]
    )

    address_in2 = DBAddress(
        id = aId2,
        customer_id = cId,
        street=streets[index2],
        city=cities[index2],
        country=countries[index1]
    )

    ins1 = customer.insert().values(**customer_in.dict())
    ins2 = address.insert().values(**address_in1.dict())
    ins3 = address.insert().values(**address_in2.dict())
    conn.execute(ins1)
    conn.execute(ins2)
    conn.execute(ins3)
