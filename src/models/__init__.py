from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_username = environ.get('DB_USERNAME')
db_password = environ.get('DB_PASSWORD')
db_hostname = environ.get('DB_HOSTNAME')
db_name = environ.get('DB_NAME')

engine = create_engine(
    f'postgresql://{db_username}:{db_password}@{db_hostname}/{db_name}')

Session = sessionmaker(bind=engine)
