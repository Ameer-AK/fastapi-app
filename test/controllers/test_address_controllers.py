import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src'))

import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from test.controllers.conftest import assertFieldRequiredException, assertTypeValidationException


@patch("controllers.address.Address.getAll")
def test_getAllAddresses(mockGetAll, client):
    mockGetAll.return_value = []

    response = client.get('/addresses')

    mockGetAll.assert_called()
    assert response.json() == []
    assert response.status_code == 200


@patch("controllers.address.Address.getAll")
def test_getAllAddresses_withQuery(mockGetAll, mock_address_request_data, client):
    mockGetAll.return_value = [mock_address_request_data.copy()]
    request_data = mock_address_request_data.copy()
    del request_data['id']
    del request_data['customer_id']

    response = client.get('/addresses/?customer_id=47dd46aa-2668-4fe6-a8db-e6a47dd63cde'
                '&street=street%20name'
                '&city=city%20name'
                '&country=country%20name')

    mockGetAll.assert_called_with(**request_data, customer_id=UUID(mock_address_request_data['customer_id']))
    assert response.json() == [mock_address_request_data]
    assert response.status_code == 200


def test_getAllAddresses_withQuery_typeValidation(client):
    response = client.get('/addresses/?customer_id=123')
    
    assertTypeValidationException("customer_id", "uuid", response=response)
    

@patch("controllers.address.Address.get")
def test_getAddress(mockGet, mock_address_request_data, client):
    mockGet.return_value = mock_address_request_data.copy()

    response = client.get('/addresses/77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a')

    mockGet.assert_called_with(id=UUID("77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a"))
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.get")
def test_getAddress_nonExistent(mockGet, mock_address_request_data, client):
    mockGet.side_effect = NoResultFound()

    response = client.get('/addresses/77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a')

    mockGet.assert_called_with(id=UUID("77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a"))
    assert response.json() == {'detail': 'Address with id: 77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a not found'}
    assert response.status_code == 404


@patch("controllers.address.Address.get")
def test_getAddress_requiredFieldValidation(mockGet, mock_address_request_data, client):
    mockGet.return_value = mock_address_request_data.copy()

    del mockGet.return_value['id']

    assertFieldRequiredException('id', route='addresses', client=client)

    mockGet.return_value['id'] = mock_address_request_data['id']
    del mockGet.return_value['customer_id']

    assertFieldRequiredException('customer_id', route='addresses', client=client)

    mockGet.return_value['customer_id'] = mock_address_request_data['customer_id']
    del mockGet.return_value['city']

    assertFieldRequiredException('city', route='addresses', client=client)

    mockGet.return_value['city'] = mock_address_request_data['city']
    del mockGet.return_value['country']

    assertFieldRequiredException('country', route='addresses', client=client)


@patch("controllers.address.Address.get")
def test_getAddress_fieldTypeValidation(mockGet, mock_address_request_data, client):
    mockGet.return_value = mock_address_request_data.copy()

    mockGet.return_value['id'] = 123

    assertTypeValidationException("id", "uuid", route="addresses", client=client)

    mockGet.return_value['id'] = UUID(mock_address_request_data['id'])
    mockGet.return_value['customer_id'] = 123

    assertTypeValidationException("customer_id", "uuid", route="addresses", client=client)


@patch("controllers.address.Address.insert")
def test_addAddress(mockInsert, mock_address_request_data, client):
    mockInsert.return_value = mock_address_request_data.copy()
    request_data = mock_address_request_data.copy()
    del request_data['id']

    response = client.post('/addresses/', json=request_data)

    request_data['customer_id'] = UUID(request_data['customer_id'])

    mockInsert.assert_called_with(**request_data)
    assert response.json() == mock_address_request_data
    assert response.status_code == 201


def test_addAddress_requiredFieldValidation(mock_address_request_data, client):
    base_request_data = mock_address_request_data.copy()
    del base_request_data['id']

    request_data = base_request_data.copy()
    del request_data['customer_id']

    response = client.post('/addresses/', json=request_data)

    assertFieldRequiredException("customer_id", response=response)

    request_data = base_request_data.copy()
    del request_data['city']

    response = client.post('/addresses/', json=request_data)

    assertFieldRequiredException("city", response=response)

    request_data = base_request_data.copy()
    del request_data['country']

    response = client.post('/addresses/', json=request_data)

    assertFieldRequiredException("country", response=response)
