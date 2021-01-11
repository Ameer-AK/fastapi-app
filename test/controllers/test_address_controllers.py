import pytest
from unittest.mock import patch
from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound


@patch("controllers.address.Address.get_all")
def test_get_addresses(mock_get_all, client, mock_address_request_data):
    mock_get_all.return_value = [mock_address_request_data.copy()]

    response = client.get('/addresses')

    mock_get_all.assert_called()
    assert response.json() == [mock_address_request_data]
    assert response.status_code == 200


@patch("controllers.address.Address.get_all")
def test_get_addresses_with_query(mock_get_all, mock_address_request_data, client):
    mock_get_all.return_value = [mock_address_request_data.copy()]
    request_data = mock_address_request_data.copy()
    del request_data['id']
    del request_data['customer_id']

    response = client.get('/addresses/?customer_id=47dd46aa-2668-4fe6-a8db-e6a47dd63cde'
                '&street=street%20name'
                '&city=city%20name'
                '&country=country%20name')

    mock_get_all.assert_called_with(**request_data, customer_id=UUID(mock_address_request_data['customer_id']))
    assert response.json() == [mock_address_request_data]
    assert response.status_code == 200


@patch("controllers.address.Address.get")
def test_get_address(mock_get, mock_address_request_data, client):
    mock_get.return_value = mock_address_request_data.copy()

    response = client.get('/addresses/77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a')

    mock_get.assert_called_with(id=UUID("77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a"))
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.get")
def test_get_address_non_existent(mock_get, mock_address_request_data, client):
    mock_get.side_effect = NoResultFound()

    response = client.get('/addresses/77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a')

    mock_get.assert_called_with(id=UUID("77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a"))
    assert response.json() == {'detail': 'Address with id: 77e2c1f3-68f8-483b-bc30-fef0b1fe0d2a not found'}
    assert response.status_code == 404


@patch("controllers.address.Address.insert")
def test_add_address(mock_insert, mock_address_request_data, client):
    mock_insert.return_value = mock_address_request_data.copy()
    request_data = mock_address_request_data.copy()
    del request_data['id']

    response = client.post('/addresses/', json=request_data)

    request_data['customer_id'] = UUID(request_data['customer_id'])

    mock_insert.assert_called_with(**request_data)
    assert response.json() == mock_address_request_data
    assert response.status_code == 201


@patch("controllers.address.Address.update")
def test_update_address(mock_update, mock_address_request_data, client):
    mock_update.return_value = mock_address_request_data.copy()

    request_data = mock_address_request_data.copy()
    del request_data['id']
    del request_data['customer_id']

    response = client.patch(f'/addresses/{mock_address_request_data["id"]}', json=request_data)

    mock_update.assert_called_with(UUID(mock_address_request_data['id']), **request_data)
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.update")
def test_update_address_non_existent(mock_update, mock_address_request_data, client):
    mock_update.side_effect = NoResultFound()

    response = client.patch(f'/addresses/{mock_address_request_data["id"]}', json={})

    mock_update.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json()['detail'] == f"Address with id: {mock_address_request_data['id']} not found"
    assert response.status_code == 404


@patch("controllers.address.Address.delete")
def test_delete_address(mock_delete, mock_address_request_data, client):
    mock_delete.return_value = mock_address_request_data.copy()

    response = client.delete(f"/addresses/{mock_address_request_data['id']}")

    mock_delete.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json() == mock_address_request_data
    assert response.status_code == 200


@patch("controllers.address.Address.delete")
def test_delete_address_non_existent(mock_delete, mock_address_request_data, client):
    mock_delete.side_effect = NoResultFound()

    response = client.delete(f"/addresses/{mock_address_request_data['id']}")

    mock_delete.assert_called_with(UUID(mock_address_request_data['id']))
    assert response.json()['detail'] == f"Address with id: {mock_address_request_data['id']} not found"
    assert response.status_code == 404
