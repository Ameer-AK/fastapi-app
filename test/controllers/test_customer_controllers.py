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
    
    assertTypeValidationException("age", "integer", response=response)

    response = client.get('/customers/?married=test')

    assertTypeValidationException("married", "bool", response=response)

    response = client.get('/customers/?height=Three')

    assertTypeValidationException("height", "float", response=response)

    response = client.get('/customers/?weight=Four')

    assertTypeValidationException("weight", "float", response=response)


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

    assertFieldRequiredException('id', client=client)

    mockGet.return_value['id'] = UUID('47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    del mockGet.return_value['first_name']

    assertFieldRequiredException('first_name', client=client)

    mockGet.return_value['first_name'] = "first name"
    del mockGet.return_value['last_name']

    assertFieldRequiredException('last_name', client=client)

    mockGet.return_value['last_name'] = "last name"
    del mockGet.return_value['married']

    assertFieldRequiredException('married', client=client)

    mockGet.return_value['married'] = True
    del mockGet.return_value['age']

    assertFieldRequiredException('age', client=client)
    
    mockGet.return_value['age'] = 50
    del mockGet.return_value['height']

    assertFieldRequiredException('height', client=client)

    mockGet.return_value['height'] = 190
    del mockGet.return_value['weight']

    assertFieldRequiredException('weight', client=client)


@patch('controllers.customer.Customer.get')
def test_getCustomer_feildTypeValidation(mockGet, mock_request_data, client):
    mockGet.return_value = mock_request_data.copy()

    mockGet.return_value['id'] = 123

    assertTypeValidationException("id", "uuid", client=client)

    mockGet.return_value['id'] = UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde")
    mockGet.return_value['married'] = "married"

    assertTypeValidationException("married", "bool", client=client)

    mockGet.return_value['married'] = True
    mockGet.return_value['age'] = "Fifty"

    assertTypeValidationException("age", "integer", client=client)

    mockGet.return_value['age'] = 50
    mockGet.return_value['height'] = "OneEighty"

    assertTypeValidationException("height", "float", client=client)

    mockGet.return_value['height'] = 180.5
    mockGet.return_value['weight'] = "Eighty"

    assertTypeValidationException("weight", "float", client=client)

    mockGet.return_value['weight'] = 80.8
    mockGet.return_value['addresses'] = "List"

    assertTypeValidationException("addresses", "list", client=client)


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
    base_request_data = mock_request_data.copy()
    del base_request_data['id']
    del base_request_data['addresses']

    request_data = base_request_data.copy()
    del request_data['first_name']

    response = client.post('/customers/', json=request_data)

    assertFieldRequiredException("first_name", response=response)

    request_data = base_request_data.copy()
    del request_data['last_name']

    response = client.post('/customers/', json=request_data)

    assertFieldRequiredException("last_name", response=response)

    request_data = base_request_data.copy()
    del request_data['age']

    response = client.post('/customers/', json=request_data)
    
    assertFieldRequiredException("age", response=response)

    request_data = base_request_data.copy()
    del request_data['height']

    response = client.post('/customers/', json=request_data)
    
    assertFieldRequiredException("height", response=response)

    request_data = base_request_data.copy()
    del request_data['weight']

    response = client.post('/customers/', json=request_data)
    
    assertFieldRequiredException("weight", response=response)

@patch('controllers.customer.Customer.insert')
def test_addCustomer_fieldTypeValidation(mockInsert, mock_request_data, client):
    mockInsert.return_value = mock_request_data.copy()
    base_request_data = mock_request_data.copy()
    del base_request_data['id']
    del base_request_data['addresses']

    request_data = base_request_data.copy()
    request_data['age'] = "Twelve"

    response = client.post('/customers/', json=request_data)
    
    assertTypeValidationException("age", "integer", response=response)

    request_data = base_request_data.copy()
    request_data['married'] = "married"

    response = client.post('/customers/', json=request_data)
    
    assertTypeValidationException("married", "bool", response=response)

    request_data = base_request_data.copy()
    request_data['height'] = "OneEighty"

    response = client.post('/customers/', json=request_data)
    
    assertTypeValidationException("height", "float", response=response)

    request_data = base_request_data.copy()
    request_data['weight'] = "NinetyTwo"

    response = client.post('/customers/', json=request_data)
    
    assertTypeValidationException("weight", "float", response=response)


@patch('controllers.customer.Customer.update')
def test_updateCustomer(mockUpdate, mock_request_data, client):
    mockUpdate.return_value = mock_request_data.copy()

    request_data = mock_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.patch(f"/customers/{mock_request_data['id']}", json=request_data)

    mockUpdate.assert_called_with(UUID(mock_request_data['id']), **request_data)

    assert response.json() == mock_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.update')
def test_updateCustomer_nonExistant(mockUpdate, mock_request_data, client):
    mockUpdate.side_effect = NoResultFound()

    response = client.patch(f"/customers/{mock_request_data['id']}", json={})
    
    assert response.json()['detail'] == f"Customer with id: {mock_request_data['id']} not found"
    assert response.status_code == 404


@patch('controllers.customer.Customer.update')
def test_updateCustomer_typeValidation(mockUpdate, mock_request_data, client):
    response = client.patch(f"/customers/{mock_request_data['id']}", json=dict(age="Twelve"))

    assertTypeValidationException("age", "integer", response=response)

    response = client.patch(f"/customers/{mock_request_data['id']}", json=dict(married="Married"))

    assertTypeValidationException("married", "bool", response=response)

    response = client.patch(f"/customers/{mock_request_data['id']}", json=dict(height="OneTwenty"))

    assertTypeValidationException("height", "float", response=response)

    response = client.patch(f"/customers/{mock_request_data['id']}", json=dict(weight="OneHundred"))

    assertTypeValidationException("weight", "float", response=response)


def assertFieldRequiredException(fieldName, client = None, response = None):
    if response is None:
        with pytest.raises(ValidationError) as e:
            response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
        error = e.value.errors()[0]
    else:
        error = response.json()['detail'][0]

    assert error["loc"][1] == fieldName
    assert error["type"] == "value_error.missing"


def assertTypeValidationException(fieldName, fieldType, client = None, response = None):
    if response is None:
        with pytest.raises(ValidationError) as e:
            response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
        error = e.value.errors()[0]
    else:
        error = response.json()['detail'][0]
    
    assert error["loc"][1] == fieldName
    assert error["type"] == f"type_error.{fieldType}"
