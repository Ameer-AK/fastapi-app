import os
import sys

sys.path.append(os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'src'))
    
import pytest
from fastapi.testclient import TestClient
from main import app

print(sys.path)

@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='module')
def mock_customer_request_data():
    return dict(
        id="47dd46aa-2668-4fe6-a8db-e6a47dd63cde",
        first_name="first name",
        middle_name="middle name",
        last_name="last name",
        married=True,
        age=30,
        height=170.5,
        weight=85.8,
        addresses=[]
    )


@pytest.fixture(scope='module')
def mock_address_request_data():
    return dict(
        id="77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a",
        customer_id="47dd46aa-2668-4fe6-a8db-e6a47dd63cde",
        street="street name",
        city="city name",
        country="country name"
    )
