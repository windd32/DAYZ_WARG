import requests
import json
import os

def update_currency(file_path: str, increment: int):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    # Открываем и читаем содержимое файла
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Изменяем значение m_OwnedCurrency
    if 'm_OwnedCurrency' in data:
        data['m_OwnedCurrency'] += increment
    else:
        print("Ключ 'm_OwnedCurrency' не найден в файле.")
        return

    # Сохраняем изменения обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    print(f"Значение m_OwnedCurrency обновлено на {increment}. Новое значение: {data['m_OwnedCurrency']}")

def process_orders(client_id: str, api_key: str):
    # Формируем URL для запроса
    api_url = f"https://api.wargm.ru/v1/shop/operations?client={client_id}:{api_key}&status=pending"
    #print(api_url)
    # Выполняем запрос к API
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Проверяем на наличие ошибок

        # Обрабатываем JSON-ответ
        data = response.json()

        # Проверяем статус ответа
        if data['responce']['status'] == 'ok':
            # Извлекаем данные о предложениях
            operations = data['responce']['data']
            data_count = data['responce']['data_count']

            print(f"Количество операций: {data_count}")

            for operation_id, operation in operations.items():
                # Извлекаем необходимые данные
                offer_id = operation['offer_id']
                user_steam_id = operation['user_steam_id']
                item_name = operation['name']  # Здесь мы получаем 'Маленькая баночка клубничного варенья'

                # Проверяем, соответствует ли имя предмета "Marmalade"
                
                print(f"ID операции: {operation['id']}")
                print(f"Offer ID: {offer_id}")
                print(f"User Steam ID: {user_steam_id}")
                print(f"Имя предмета: {item_name}")
                print(f"Игрок: {operation['player']}")
                print(f"Статус: {operation['status']}")
                print(f"Цена: {operation['price']} {operation['cy']}")
                print("-" * 30)  # Разделитель между операциями
                
                if offer_id == 210815:  
                    print("Покупка 100рублей") 
                    increment_value = 100  # Значение, которое нужно прибавить
                    file_path = f"C:\\Dayz\\profiles\\DC_Banking\\PlayerDatabase\\{user_steam_id}.json"
                    update_currency(file_path, increment_value)
                    confirm_url = f"https://api.wargm.ru/v1/shop/operation_success?operation_id={operation['id']}&client={client_id}:{api_key}"
                    #print(confirm_url)
                    confirm_response = requests.get(confirm_url)
                    # Выводим ответ от сервера
                    #print(f"Ответ от сервера при подтверждении операции: {confirm_response.text}")
                    # Проверяем ответ на запрос подтверждения
                    confirm_data = confirm_response.json() if confirm_response.text else {}
                    if confirm_data.get('responce', {}).get('status') == 'ok':
                        print("Запрос на подтверждение операции выполнен.")
                    else:
                        for _ in range(5):
                            print(f"Ошибка при подтверждении операции: {confirm_data.get('responce', {}).get('msg', 'Неизвестная ошибка')}")



        else:
            print("Ошибка в ответе API:", data['responce']['status'])

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")



# Пример использования
client_id = '48'  # Замените на ваш client_id
api_key = '!OEiyP_F6'      # Замените на ваш api_key
process_orders(client_id, api_key)
