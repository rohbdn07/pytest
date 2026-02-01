import requests

BASE_URL = "https://dummyjson.com"

def test_get_product():
    response = requests.get(BASE_URL)
    assert response.status_code == 200

def test_get_allProducts():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    json_data = response.json()