import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from test.conftest import assertFieldRequiredException, assertTypeValidationException


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


def test_getAllCustomers_withQuery_typeValidation(client):
    response = client.get('/customers/?age=Twelve')
    
    assertTypeValidationException("age", "integer", response=response)

    response = client.get('/customers/?married=test')

    assertTypeValidationException("married", "bool", response=response)

    response = client.get('/customers/?height=Three')

    assertTypeValidationException("height", "float", response=response)

    response = client.get('/customers/?weight=Four')

    assertTypeValidationException("weight", "float", response=response)


@patch('controllers.customer.Customer.get')
def test_getCustomer(mockGet, mock_customer_request_data, client):
    mockGet.return_value = mock_customer_request_data.copy()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    
    mockGet.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.get')
def test_getCustomer_nonExistent(mockGet, client):
    mockGet.side_effect = NoResultFound()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')

    mockGet.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == {'detail': 'Customer with id: 47dd46aa-2668-4fe6-a8db-e6a47dd63cde not found'}
    assert response.status_code == 404


@patch('controllers.customer.Customer.get')
def test_getCustomer_ageValidation(mockGet, mock_customer_request_data, client):
    mockGet.return_value = mock_customer_request_data.copy()

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
def test_getCustomer_requiredFieldValidation(mockGet, mock_customer_request_data, client):
    mockGet.return_value = mock_customer_request_data.copy()

    del mockGet.return_value['id']

    assertFieldRequiredException('id', route = 'customers', client=client)

    mockGet.return_value['id'] = UUID(mock_customer_request_data['id'])
    del mockGet.return_value['first_name']

    assertFieldRequiredException('first_name', route = 'customers', client=client)

    mockGet.return_value['first_name'] = mock_customer_request_data['first_name']
    del mockGet.return_value['last_name']

    assertFieldRequiredException('last_name', route = 'customers', client=client)

    mockGet.return_value['last_name'] = mock_customer_request_data['last_name']
    del mockGet.return_value['married']

    assertFieldRequiredException('married', route = 'customers', client=client)

    mockGet.return_value['married'] = mock_customer_request_data['married']
    del mockGet.return_value['age']

    assertFieldRequiredException('age', route = 'customers', client=client)
    
    mockGet.return_value['age'] = mock_customer_request_data['age']
    del mockGet.return_value['height']

    assertFieldRequiredException('height', route = 'customers', client=client)

    mockGet.return_value['height'] = mock_customer_request_data['height']
    del mockGet.return_value['weight']

    assertFieldRequiredException('weight', route = 'customers', client=client)


@patch('controllers.customer.Customer.get')
def test_getCustomer_feildTypeValidation(mockGet, mock_customer_request_data, client):
    mockGet.return_value = mock_customer_request_data.copy()

    mockGet.return_value['id'] = 123

    assertTypeValidationException("id", "uuid", route = 'customers', client=client)

    mockGet.return_value['id'] = UUID(mock_customer_request_data['id'])
    mockGet.return_value['married'] = "married"

    assertTypeValidationException("married", "bool", route = 'customers', client=client)

    mockGet.return_value['married'] = mock_customer_request_data['married']
    mockGet.return_value['age'] = "Fifty"

    assertTypeValidationException("age", "integer", route = 'customers', client=client)

    mockGet.return_value['age'] = mock_customer_request_data['age']
    mockGet.return_value['height'] = "OneEighty"

    assertTypeValidationException("height", "float", route = 'customers', client=client)

    mockGet.return_value['height'] = mock_customer_request_data['height']
    mockGet.return_value['weight'] = "Eighty"

    assertTypeValidationException("weight", "float", route = 'customers', client=client)

    mockGet.return_value['weight'] = mock_customer_request_data['weight']
    mockGet.return_value['addresses'] = "List"

    assertTypeValidationException("addresses", "list", route = 'customers', client=client)


@patch('controllers.customer.Customer.insert')
def test_addCustomer(mockInsert, mock_customer_request_data, client):
    mockInsert.return_value = mock_customer_request_data.copy()
    request_data = mock_customer_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.post('/customers/', json=request_data)
    
    mockInsert.assert_called_with(**request_data)
    assert response.json() == mock_customer_request_data
    assert response.status_code == 201


def test_addCustomer_requiredFieldValidation(mock_customer_request_data, client):
    base_request_data = mock_customer_request_data.copy()
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


def test_addCustomer_fieldTypeValidation(mock_customer_request_data, client):
    base_request_data = mock_customer_request_data.copy()
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
def test_updateCustomer(mockUpdate, mock_customer_request_data, client):
    mockUpdate.return_value = mock_customer_request_data.copy()

    request_data = mock_customer_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=request_data)

    mockUpdate.assert_called_with(UUID(mock_customer_request_data['id']), **request_data)
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.update')
def test_updateCustomer_nonExistent(mockUpdate, mock_customer_request_data, client):
    mockUpdate.side_effect = NoResultFound()

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json={})
    
    mockUpdate.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json()['detail'] == f"Customer with id: {mock_customer_request_data['id']} not found"
    assert response.status_code == 404


def test_updateCustomer_typeValidation(mock_customer_request_data, client):
    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=dict(age="Twelve"))

    assertTypeValidationException("age", "integer", response=response)

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=dict(married="Married"))

    assertTypeValidationException("married", "bool", response=response)

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=dict(height="OneTwenty"))

    assertTypeValidationException("height", "float", response=response)

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=dict(weight="OneHundred"))

    assertTypeValidationException("weight", "float", response=response)


@patch('controllers.customer.Customer.delete')
def test_deleteCustomer(mockDelete, mock_customer_request_data, client):
    mockDelete.return_value = mock_customer_request_data.copy()

    response = client.delete(f"/customers/{mock_customer_request_data['id']}")
    
    mockDelete.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.delete')
def test_deleteCustomer_nonExistent(mockDelete, mock_customer_request_data, client):
    mockDelete.side_effect = NoResultFound()

    response = client.delete(f"/customers/{mock_customer_request_data['id']}")

    mockDelete.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json()['detail'] == f"Customer with id: {mock_customer_request_data['id']} not found"
    assert response.status_code == 404


