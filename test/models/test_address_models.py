import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src'))

from unittest.mock import patch
from models.address import Address

@patch('models.engine')
def test_as_json(mockEngine, mock_address_request_data):
    mock_address_request_data['created_at'] = None
    mock_address_request_data['last_updated'] = None
    
    address = Address(**mock_address_request_data)

    assert address.as_json() == mock_address_request_data