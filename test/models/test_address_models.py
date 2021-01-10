import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src'))

from unittest.mock import patch
from models.address import Address

@patch('models.engine')
def test_as_json(mockEngine, mock_address_request_data):
    request_data = mock_address_request_data.copy()
    request_data['created_at'] = None
    request_data['last_updated'] = None

    address = Address(**request_data)

    assert address.as_json() == request_data