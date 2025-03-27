import requests

def test_api_endpoint():
    response = requests.get("http://localhost:5000/api/data")
    assert response.status_code == 200
