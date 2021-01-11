import pytest
from unittest.mock import patch, Mock
from models.base_model import BaseModel

@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_getAll(mockSession, mock_as_json, mock_address_request_data):
    queryCall = mockSession.return_value.query
    filterCall = queryCall.return_value.filter_by

    filterCall.return_value.all.return_value = [BaseModel()]
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().getAll(**mock_address_request_data)

    queryCall.assert_called_with(BaseModel)
    filterCall.assert_called_with(**mock_address_request_data)
    assert result == [mock_address_request_data]
    

@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_get(mockSession, mock_as_json, mock_address_request_data):
    queryCall = mockSession.return_value.query
    filterCall = queryCall.return_value.filter_by

    filterCall.return_value.one.return_value = BaseModel()
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().get(123)

    queryCall.assert_called_with(BaseModel)
    filterCall.assert_called_with(id=123)
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_insert(mockSession, mock_as_json, mock_address_request_data):
    addCall = mockSession.return_value.add
    commitCall = mockSession.return_value.commit
    
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().insert()

    addCall.assert_called()
    commitCall.assert_called()
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_update(mockSession, mock_as_json, mock_address_request_data):
    queryCall = mockSession.return_value.query
    filterCall = queryCall.return_value.filter_by
    commitCall = mockSession.return_value.commit

    filterCall.return_value.one.return_value = BaseModel()
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().update(id=123, name="test")

    queryCall.assert_called_with(BaseModel)
    filterCall.assert_called_with(id=123)
    commitCall.assert_called()
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_delete(mockSession, mock_as_json, mock_address_request_data):
    queryCall = mockSession.return_value.query
    filterCall = queryCall.return_value.filter_by
    commitCall = mockSession.return_value.commit
    deleteCall = mockSession.return_value.delete

    model = BaseModel()

    filterCall.return_value.one.return_value = model
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().delete(id=123)

    queryCall.assert_called_with(BaseModel)
    filterCall.assert_called_with(id=123)
    deleteCall.assert_called_with(model)
    commitCall.assert_called()
    assert result == mock_address_request_data

def test_as_json():
    with pytest.raises(Exception):
        BaseModel().as_json()