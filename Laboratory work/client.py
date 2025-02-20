import requests  # Импортируем модуль для выполнения HTTP-запросов
from requests.auth import HTTPBasicAuth   # Импортируем модуль для базовой аутентификации
from unittest.mock import patch  # Импортируем patch из модуля unittest.mock для создания заглушек

# Конфигурация сервера
BASE_URL = 'http://localhost:8000'
USERNAME = 'admin'
PASSWORD = 'password'


# Функция для выполнения GET-запроса к серверу
def get_request():
    # Отправляем GET-запрос с аутентификацией
    response = requests.get(BASE_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(f'Sever URL: {response.url}', end='\n\n')  # Выводим URL, к которому был отправлен запрос
    print(f'GET Response: {response.status_code} - {response.text}')  # Выводим статус-код и текст ответа
    print(f'GET Response Headers: {response.headers}')  # Выводим заголовки ответа
    print(f'Cache-Control: {response.headers.get("Cache-Control")}', end='\n\n') # Выводим значение заголовка Cache-Control


# Функция для выполнения POST-запроса
def post_request(data):
    # Отправляем POST-запрос с аутентификацией
    response = requests.post(BASE_URL, data=data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(f'POST Response: {response.status_code} - {response.text}')  # Выводим статус-код и текст ответа
    print(f'POST Response Headers: {response.headers}')  # Выводим заголовки ответа
    print(f'Cache-Control: {response.headers.get("Cache-Control")}', end='\n\n')  # Печатает значение заголовка Cache-Control


# Функция для выполнения PUT-запроса
def put_request(data):
    # Отправляем PUT-запрос с аутентификацией
    response = requests.put(BASE_URL, data=data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(f'PUT Response: {response.status_code} - {response.text}')  # Выводим статус-код и текст ответа
    print(f'PUT Response Headers: {response.headers}')  # Выводим заголовки ответа
    print(f'Cache-Control: {response.headers.get("Cache-Control")}', end='\n\n')  # Печатает значение заголовка Cache-Control


# Функция для выполнения DELETE-запроса
def delete_request():
    # Отправляем DELETE-запрос с аутентификацией
    response = requests.delete(BASE_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(f'DELETE Response: {response.status_code} - {response.text}')  # Выводим статус-код и текст ответа
    print(f'DELETE Response Headers: {response.headers}')  # Выводим заголовки ответа
    print(f'Cache-Control: {response.headers.get("Cache-Control")}', end='\n\n')  # Печатает значение заголовка Cache-Control


# Функция для получения данных без запроса к серверу (используем заглушку mock)
def no_server_get_data():
    url = ""  # пустая строка вместо URL, т.к. на сервер запрос не отправляем
    mock_response = {"my_key": "my_value"}  # Имитация ответа от сервера в виде словаря

    # Используем patch для замены requests.get на заглушку
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response  # Настраиваем заглушку, чтобы она возвращала mock_response
        result = requests.get(url).json()  # Выполняем GET-запрос и возвращаем ответ в формате JSON
        print('Repeated GET without a request to the server :', result)  # Выводим результат на экран; ожидаемый вывод: {'my_key': 'my_value'}


# Выполнение запросов
get_request()  # Вызов функции для выполнения GET-запроса
post_request('Hello, World!')  # Вызов функции для выполнения POST-запроса
put_request('Updated data!')  # Вызов функции для выполнения PUT-запроса
delete_request()  # Вызов функции для выполнения DELETE-запроса
no_server_get_data() # Вызов функции для выполнения GET-запроса без запроса к серверу
