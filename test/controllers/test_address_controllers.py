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
    
