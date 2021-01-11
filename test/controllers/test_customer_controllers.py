import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound


@patch('controllers.customer.Customer.get_all')
def test_get_customers(mock_get_all, client, mock_customer_request_data):
    mock_get_all.return_value = [mock_customer_request_data.copy()]

    response = client.get('/customers')

    mock_get_all.assert_called()
    assert response.json() == [mock_customer_request_data]
    assert response.status_code == 200


@patch('controllers.customer.Customer.get_all')
def test_get_customers_with_query(mock_get_all, client, mock_customer_request_data):
    mock_get_all.return_value = [mock_customer_request_data]

    response = client.get('/customers/?first_name=testFirstName'
        '&middle_name=testMiddleName&last_name=testLastName&'
        'age=50&married=true&height=150.5&weight=150.8')

    mock_get_all.assert_called_with(
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
def test_get_customer(mock_get, mock_customer_request_data, client):
    mock_get.return_value = mock_customer_request_data.copy()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')
    
    mock_get.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.get')
def test_get_customer_non_existent(mock_get, client):
    mock_get.side_effect = NoResultFound()

    response = client.get('/customers/47dd46aa-2668-4fe6-a8db-e6a47dd63cde')

    mock_get.assert_called_with(id=UUID("47dd46aa-2668-4fe6-a8db-e6a47dd63cde"))
    assert response.json() == {'detail': 'Customer with id: 47dd46aa-2668-4fe6-a8db-e6a47dd63cde not found'}
    assert response.status_code == 404


@patch('controllers.customer.Customer.insert')
def test_add_customer(mock_insert, mock_customer_request_data, client):
    mock_insert.return_value = mock_customer_request_data.copy()
    request_data = mock_customer_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.post('/customers/', json=request_data)
    
    mock_insert.assert_called_with(**request_data)
    assert response.json() == mock_customer_request_data
    assert response.status_code == 201


@patch('controllers.customer.Customer.update')
def test_update_customer(mock_update, mock_customer_request_data, client):
    mock_update.return_value = mock_customer_request_data.copy()

    request_data = mock_customer_request_data.copy()
    del request_data['id']
    del request_data['addresses']

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json=request_data)

    mock_update.assert_called_with(UUID(mock_customer_request_data['id']), **request_data)
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.update')
def test_update_customer_non_existent(mock_update, mock_customer_request_data, client):
    mock_update.side_effect = NoResultFound()

    response = client.patch(f"/customers/{mock_customer_request_data['id']}", json={})
    
    mock_update.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json()['detail'] == f"Customer with id: {mock_customer_request_data['id']} not found"
    assert response.status_code == 404


@patch('controllers.customer.Customer.delete')
def test_delete_customer(mock_delete, mock_customer_request_data, client):
    mock_delete.return_value = mock_customer_request_data.copy()

    response = client.delete(f"/customers/{mock_customer_request_data['id']}")
    
    mock_delete.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json() == mock_customer_request_data
    assert response.status_code == 200


@patch('controllers.customer.Customer.delete')
def test_delete_customer_non_existent(mock_delete, mock_customer_request_data, client):
    mock_delete.side_effect = NoResultFound()

    response = client.delete(f"/customers/{mock_customer_request_data['id']}")

    mock_delete.assert_called_with(UUID(mock_customer_request_data['id']))
    assert response.json()['detail'] == f"Customer with id: {mock_customer_request_data['id']} not found"
    assert response.status_code == 404
