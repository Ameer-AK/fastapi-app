from unittest.mock import patch
from models.customer import Customer

@patch('models.engine')
def test_as_json(mockEngine, mock_customer_request_data):
    request_data = mock_customer_request_data.copy()    

    customer = Customer(**request_data)

    request_data['created_at'] = None
    request_data['last_updated'] = None
    
    assert customer.as_json() == request_data