def test_home(client):
    response = client.get('/')

    assert response.json() == "Hello"
    assert response.status_code == 200