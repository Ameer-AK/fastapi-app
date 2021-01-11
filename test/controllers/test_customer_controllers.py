import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound


@patch('controllers.customer.Customer.getAll')
def test_getAllCustomers(mockGetAll, client, mock_customer_request_data):
    mockGetAll.return_value = [mock_customer_request_data.copy()]

    response = client.get('/customers')

    mockGetAll.assert_called()
    assert response.json() == [mock_customer_request_data]
    assert response.status_code == 200


@patch('controllers.customer.Customer.getAll')
def test_getAllCustomers_withQuery(mockGetAll, client, mock_customer_request_data):
    mockGetAll.return_value = [mock_customer_request_data]

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
    assert response.json() == [mock_customer_request_data]
    assert response.status_code == 200


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
