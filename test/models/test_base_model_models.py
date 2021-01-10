import pytest
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel


@patch('models.base_model.Session')
def test_getAll(mockSession, mock_address_request_data):
    queryCall = mockSession.return_value.query

    filterCall = queryCall.return_value.filter_by

    filterCall.return_value.all.return_value = []

    result = BaseModel().getAll(**mock_address_request_data)

    queryCall.assert_called_with(BaseModel)
    filterCall.assert_called_with(**mock_address_request_data)
    assert result == []
    

@patch('models.base_model.Session')
def test_get(mockSession):
    pass