#pip install requests
import requests

# Задаем параметры
client_id = '408'  # Замените на ваш client_id
api_key = '!'      # Замените на ваш api_key

# Формируем URL для запроса
api_url = f"https://api.wargm.ru/v1/shop/operations?client={client_id}:{api_key}&status=pending"
 
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

            # Проверяем, соответствует ли имя предмета "Мarmalade"
            if item_name == "Маленькая баночка клубничного варенья":
                print(f"ID операции: {operation['id']}")
                print(f"Offer ID: {offer_id}")
                print(f"User Steam ID: {user_steam_id}")
                print(f"Имя предмета: {item_name}")
                print(f"Игрок: {operation['player']}")
                print(f"Статус: {operation['status']}")
                print(f"Цена: {operation['price']} {operation['cy']}")
                print("-" * 30)  # Разделитель между операциями
                
                # Отправляем запрос на подтверждение операции
                confirm_url = f"https://api.wargm.ru/v1/shop/operation_success?operation_id={operation['id']}&client={client_id}:{api_key}"
                print("Ответ сервера:", confirm_url)
                confirm_response = requests.GET(confirm_url)

                # Проверяем ответ на запрос подтверждения
                if confirm_response.status_code == 200:
                    confirm_data = confirm_response.json()
                    print("Запрос на подтверждение операции выполнен.")
                    print("Ответ сервера:", confirm_data)
                else:
                    print("Ошибка при подтверждении операции:", confirm_response.status_code)

    else:
        print("Ошибка в ответе API:", data['responce']['status'])

except requests.exceptions.RequestException as e:
    print(f"Произошла ошибка при выполнении запроса: {e}")
