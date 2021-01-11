import pytest
from unittest.mock import patch
from models.base_model import BaseModel

@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_get_all(MockSession, mock_as_json, mock_address_request_data):
    query_call = MockSession.return_value.query
    filter_call = query_call.return_value.filter_by

    filter_call.return_value.all.return_value = [BaseModel()]
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().get_all(**mock_address_request_data)

    query_call.assert_called_with(BaseModel)
    filter_call.assert_called_with(**mock_address_request_data)
    assert result == [mock_address_request_data]
    

@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_get(MockSession, mock_as_json, mock_address_request_data):
    query_call = MockSession.return_value.query
    filter_call = query_call.return_value.filter_by

    filter_call.return_value.one.return_value = BaseModel()
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().get(123)

    query_call.assert_called_with(BaseModel)
    filter_call.assert_called_with(id=123)
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_insert(MockSession, mock_as_json, mock_address_request_data):
    add_call = MockSession.return_value.add
    commit_call = MockSession.return_value.commit
    
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().insert()

    add_call.assert_called()
    commit_call.assert_called()
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_update(MockSession, mock_as_json, mock_address_request_data):
    query_call = MockSession.return_value.query
    filter_call = query_call.return_value.filter_by
    commit_call = MockSession.return_value.commit

    filter_call.return_value.one.return_value = BaseModel()
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().update(id=123, name="test")

    query_call.assert_called_with(BaseModel)
    filter_call.assert_called_with(id=123)
    commit_call.assert_called()
    assert result == mock_address_request_data


@patch('models.base_model.BaseModel.as_json')
@patch('models.base_model.Session')
def test_delete(MockSession, mock_as_json, mock_address_request_data):
    query_call = MockSession.return_value.query
    filter_call = query_call.return_value.filter_by
    commit_call = MockSession.return_value.commit
    delete_call = MockSession.return_value.delete

    model = BaseModel()

    filter_call.return_value.one.return_value = model
    mock_as_json.return_value = mock_address_request_data

    result = BaseModel().delete(id=123)

    query_call.assert_called_with(BaseModel)
    filter_call.assert_called_with(id=123)
    delete_call.assert_called_with(model)
    commit_call.assert_called()
    assert result == mock_address_request_data

def test_as_json():
    with pytest.raises(Exception):
        BaseModel().as_json()