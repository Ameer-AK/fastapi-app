import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound


@patch("controllers.address.Address.getAll")
def test_getAllAddresses(mockGetAll, client, mock_address_request_data):
    mockGetAll.return_value = [mock_address_request_data.copy()]

    response = client.get('/addresses')

    mockGetAll.assert_called()
    assert response.json() == [mock_address_request_data]
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


@patch("controllers.address.Address.update")
def test_updateAddress(mockUpdate, mock_address_request_data, client):
    mockUpdate.return_value = mock_address_request_data.copy()

    request_data = mock_address_request_data.copy()
    del request_data['id']
    del request_data['customer_id']

    response = client.patch(f'/addresses/{mock_address_request_data["id"]}', json=request_data)

    mockUpdate.assert_called_with(UUID(mock_address_request_data['id']), **request_data)
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.update")
def test_updateAddress_nonExistent(mockUpdate, mock_address_request_data, client):
    mockUpdate.side_effect = NoResultFound()

    response = client.patch(f'/addresses/{mock_address_request_data["id"]}', json={})

    mockUpdate.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json()['detail'] == f"Address with id: {mock_address_request_data['id']} not found"
    assert response.status_code == 404


@patch("controllers.address.Address.delete")
def test_deleteAddress(mockDelete, mock_address_request_data, client):
    mockDelete.return_value = mock_address_request_data.copy()

    response = client.delete(f"/addresses/{mock_address_request_data['id']}")

    mockDelete.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.delete")
def test_deleteAddress_nonExistent(mockDelete, mock_address_request_data, client):
    mockDelete.side_effect = NoResultFound()

    response = client.delete(f"/addresses/{mock_address_request_data['id']}")

    mockDelete.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json()['detail'] == f"Address with id: {mock_address_request_data['id']} not found"
    assert response.status_code == 404
