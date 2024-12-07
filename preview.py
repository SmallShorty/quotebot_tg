import requests

# Формируем URL с параметрами
url = "http://api.forismatic.com/api/1.0/"

# Параметры запроса
params = {
    "method": "getQuote",  # Метод API для получения цитаты
    "format": "json",  # Формат ответа JSON
    "lang": "ru",  # Язык ответа (русский)
}

# Отправляем GET-запрос с параметрами в URL
response = requests.get(url, params=params)

# Проверяем, что запрос выполнен успешно
if response.status_code == 200:
    # Преобразуем ответ в JSON
    quote_data = response.json()

    # Извлекаем цитату и автора
    quote_text = quote_data.get("quoteText", "Цитата не найдена.")
    quote_author = quote_data.get("quoteAuthor", "Неизвестный автор")

    # Выводим цитату
    print(f"Цитата: {quote_text}")
    print(f"Автор: {quote_author}")
else:
    print("Ошибка при запросе цитаты.")
