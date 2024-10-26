import requests
import json

def api_clients(contract_number):
    # URL API, откуда получаем данные
    api_url = 'http://localhost:8000/api/clients'

    # Отправляем GET-запрос к API
    response = requests.get(api_url)

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        # Преобразуем JSON-ответ в Python-словарь
        data = response.json()
        
        # Ищем значение contract_number среди contract_number
        contract_number = str(contract_number)
        for item in data:
            if item.get('contract_number') == contract_number:
                print(f"Найден contract_number: {item['contract_number']}")
                # Здесь можно добавить дополнительную логику, например, сохранение результата
                return True
        else:
            print(f"Значение {contract_number} не найдено среди contract_number")
            return False
    else:
        print(f"Ошибка при запросе к API: {response.status_code}")