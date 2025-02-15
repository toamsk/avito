import requests
import uuid

# Создание объявления с валидными данными
def test_create_ad_valid():
    url = "https://qa-internship.avito.com/api/1/item"
    payload = {
        "sellerID": 4572565,
        "name": "продам слона",
        "price": 125000
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"].startswith('Сохранили')

# Извлечение ID из строки 'Сохранили - ID'
    saved_id = response_data["status"].split(' - ')[1]

# Проверка, что ID является валидным UUID
    try:
        uuid_obj = uuid.UUID(saved_id, version=4)
    except ValueError:
        assert False, f"ID {saved_id} не является валидным UUID"

def test_create_ad_invalid():
    url = "https://qa-internship.avito.com/ads"
    payload = {
        "title": "",
        "description": "This is a sample ad",
        "price": 100,
        "sellerID": 7087526064
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400

    response_data = response.json()
    assert "error" in response_data
    assert response_data["error"] == "Invalid data"


# Создание объявления с невалидными данными
def test_create_ad_invalid():
    url = "https://qa-internship.avito.com/api/1/item"
    payload = {
        "sellerID": 708752,
        "name": "продам ноутбук",
        "price": "пятьдесят тысяч"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400


# Получение объявления по валидному идентификатору
def test_get_ad_valid():
    # Сначала создаем объявление
    create_url = "https://qa-internship.avito.com/api/1/item"
    create_payload = {
        "sellerID": 4572565,
        "name": "продам слона",
        "price": 125000
    }
    create_response = requests.post(create_url, json=create_payload)
    assert create_response.status_code == 200
    create_response_data = create_response.json()
    saved_id = create_response_data["status"].split(' - ')[1]

    # Затем получаем объявление по сохраненному ID
    get_url = f"https://qa-internship.avito.com/api/1/items/{saved_id}"
    get_response = requests.get(get_url)
    assert get_response.status_code == 200


# Получение объявления по невалидному идентификатору
def test_get_ad_invalid():
    url = "https://qa-internship.avito.com/api/1/items/0"
    response = requests.get(url)
    assert response.status_code == 404


# Получение всех объявлений по валидному идентификатору продавца
def test_get_all_ads_valid():
    url = "https://qa-internship.avito.com/api/1/seller/457000/items"
    response = requests.get(url)
    assert response.status_code == 200
    

# Получение всех объявлений по невалидному идентификатору продавца
def test_get_all_ads_invalid():
    url = "https://qa-internship.avito.com/api/1/seller/0/items"
    response = requests.get(url)
    assert response.status_code == 404


# Получение статистики по валидному itemID
def test_get_stats_valid():
    url = "https://qa-internship.avito.com/api/1/457000/item"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.content}")
    assert response.status_code == 200


# Получение статистики по невалидному itemID
def test_get_stats_invalid():
    url = "https://qa-internship.avito.com/api/1/stats/0"
    response = requests.get(url)
    assert response.status_code == 404    