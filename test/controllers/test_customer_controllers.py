import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src'))

import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from fastapi.testclient import TestClient
from sqlalchemy.orm.exc import NoResultFound
from models.customer import Customer


@patch('controllers.customer.Customer.getAll')
def test_getAllCustomers(mockGetAll, client):
    mockGetAll.return_value = []

    response = client.get('/customers')

    mockGetAll.assert_called()
    assert response.json() == []
    assert response.status_code == 200


@patch('controllers.customer.Customer.getAll')
def test_getAllCustomers_withQuery(mockGetAll, client):
    mockGetAll.return_value = []

    response = client.get('/customers/?first_name=testFirstName'
        '&middle_name=testMiddleName&last_name=testLastName&'
        'age=50&married=true&height=150.5&weight=150.8')

    mockGetAll.assert_called_with(
        first_name='testFirstName',
        middle_name='testMiddleName',
        last_name='testLastName',
        age=50,
        married=True,
        height=150.5,
        weight=150.8
    )
    assert response.json() == []
    assert response.status_code == 200


@patch('controllers.customer.Customer.getAll')
def test_getAllCustomers_withQuery_typeValidation(mockGetAll, client):
    mockGetAll.return_value = []

    response = client.get('/customers/?age=Twelve')

    assertQueryTypeValidationException(response, "age", "integer")

    response = client.get('/customers/?married=test')

    assertQueryTypeValidationException(response, "married", "bool")

    response = client.get('/customers/?height=Three')

    assertQueryTypeValidationException(response, "height", "float")

    response = client.get('/customers/?weight=Four')

    assertQueryTypeValidationException(response, "weight", "float")


@patch('controllers.customer.Customer.get')
def test_getCustomer(mockGet, mock_request_data, client):
    mockGet.return_value = mock_request_data.copy()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    
    mockGet.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == mock_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.get')
def test_getCustomer_nonExistant(mockGet, client):
    mockGet.side_effect = NoResultFound()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')

    mockGet.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == {'detail': 'Customer with id: 47dd46aa-2668-4fe6-a8db-e6a47dd63cde not found'}
    assert response.status_code == 404


@patch('controllers.customer.Customer.get')
def test_getCustomer_ageValidation(mockGet, mock_request_data, client):
    mockGet.return_value = mock_request_data.copy()

    mockGet.return_value["age"] = 500

    with pytest.raises(ValidationError) as e:
        response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    error = e.value.errors()[0]
    
    assert error["loc"] == ("response", "age")
    assert error["type"] == "value_error.number.not_lt"
    assert error["ctx"]["limit_value"] == 100

    mockGet.return_value["age"] = 0

    with pytest.raises(ValidationError) as e:
        response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    error = e.value.errors()[0]
    
    assert error["loc"] == ("response", "age")
    assert error["type"] == "value_error.number.not_gt"
    assert error["ctx"]["limit_value"] == 0

@patch('controllers.customer.Customer.get')
def test_getCustomer_requiredFieldValidation(mockGet, mock_request_data, client):
    mockGet.return_value = mock_request_data.copy()

    del mockGet.return_value['id']

    assertBodyFieldRequiredException('id', client)

    mockGet.return_value['id'] = UUID('47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    del mockGet.return_value['first_name']

    assertBodyFieldRequiredException('first_name', client)

    mockGet.return_value['first_name'] = "first name"
    del mockGet.return_value['last_name']

    assertBodyFieldRequiredException('last_name', client)

    mockGet.return_value['last_name'] = "last name"
    del mockGet.return_value['married']

    assertBodyFieldRequiredException('married', client)

    mockGet.return_value['married'] = True
    del mockGet.return_value['age']

    assertBodyFieldRequiredException('age', client)
    
    mockGet.return_value['age'] = 50
    del mockGet.return_value['height']

    assertBodyFieldRequiredException('height', client)

    mockGet.return_value['height'] = 190
    del mockGet.return_value['weight']

    assertBodyFieldRequiredException('weight', client)


@patch('controllers.customer.Customer.get')
def test_getCustomer_feildTypeValidation(mockGet, mock_request_data, client):
    mockGet.return_value = mock_request_data.copy()

    mockGet.return_value['id'] = 123

    assertBodyTypeValidationException("id", "uuid", client)

    mockGet.return_value['id'] = UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde")
    mockGet.return_value['married'] = "married"

    assertBodyTypeValidationException("married", "bool", client)

    mockGet.return_value['married'] = True
    mockGet.return_value['age'] = "Fifty"

    assertBodyTypeValidationException("age", "integer", client)

    mockGet.return_value['age'] = 50
    mockGet.return_value['height'] = "OneEighty"

    assertBodyTypeValidationException("height", "float", client)

    mockGet.return_value['height'] = 180.5
    mockGet.return_value['weight'] = "Eighty"

    assertBodyTypeValidationException("weight", "float", client)

    mockGet.return_value['weight'] = 80.8
    mockGet.return_value['addresses'] = "List"

    assertBodyTypeValidationException("addresses", "list", client)


@patch('controllers.customer.Customer.insert')
def test_addCustomer(mockInsert, mock_request_data, client):
    mockInsert.return_value = mock_request_data.copy()
    request_data = mock_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.post('/customers/', json=request_data)
    
    mockInsert.assert_called_with(**request_data)
    assert response.json() == mock_request_data
    assert response.status_code == 201


@patch('controllers.customer.Customer.insert')
def test_addCustomer_requiredFieldValidation(mockInsert, mock_request_data, client):
    mockInsert.return_value = mock_request_data.copy()
    request_data = mock_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    # del request_data

    response = client.post('/customers/', json=request_data)

    

def assertQueryTypeValidationException(response, fieldName, fieldType):
    error = response.json()['detail'][0]

    assert error['loc'] == ['query', fieldName]
    assert error['type'] == f'type_error.{fieldType}'


def assertBodyFieldRequiredException(fieldName, client):
    with pytest.raises(ValidationError) as e:
        response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    error = e.value.errors()[0]

    assert error["loc"] == ("response", fieldName)
    assert error["type"] == "value_error.missing"


def assertBodyTypeValidationException(fieldName, fieldType, client):
    with pytest.raises(ValidationError) as e:
        response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    error = e.value.errors()[0]
    
    assert error["loc"] == ("response", fieldName)
    assert error["type"] == f"type_error.{fieldType}"
