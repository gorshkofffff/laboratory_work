import http.server  # Импортируем модуль для создания HTTP-сервера
import socketserver  # Импортируем модуль для работы с сокетами
import base64  # Импортируем модуль для работы с кодированием в base64

PORT = 8000  # Устанавливаем порт, на котором будет работать сервер


# Определяем класс обработчика, наследующий от SimpleHTTPRequestHandler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Указываем пользователя для авторизации
    USERNAME = 'admin'
    # Указываем пароль пользователя для авторизации
    PASSWORD = 'password'

    # Метод для отправки HTTP-ответа с заданным кодом и сообщением
    def _send_response(self, code, message):
        self.send_response(code)  # Отправляем код ответа
        self.send_header('Content-type', 'text/plain')  # Указываем тип контента
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')  # Заголовок для кэширования
        self.send_header('Pragma', 'no-cache')  # Дополнительный заголовок для кэширования
        self.send_header('Expires', '0')  # Устанавливаем время истечения кэша
        self.end_headers()  # Завершаем заголовки
        self.wfile.write(message.encode('utf-8'))  # Отправляем сообщение в ответ

# Метод для обработки GET-запросов
    def do_GET(self):
        if not self.authenticate():  # Проверяем авторизацию
            return  # Если авторизация не прошла, выходим из метода
        self._send_response(200, 'GET request processed')  # Отправляем успешный ответ

# Метод для обработки POST-запросов
    def do_POST(self):
        if not self.authenticate():  # Проверяем авторизацию
            return  # Если авторизация не прошла, выходим из метода
        content_length = int(self.headers['Content-Length'])   # Получаем длину содержимого из заголовков
        post_data = self.rfile.read(content_length)  # Читаем данные из запроса
        self._send_response(200, f'POST request processed with data: {post_data.decode("utf-8")}')  # Отправляем успешный ответ

# Метод для обработки PUT-запросов
    def do_PUT(self):
        if not self.authenticate():  # Проверяем авторизацию
            return  # Если авторизация не прошла, выходим из метода
        content_length = int(self.headers['Content-Length'])  # Получаем длину содержимого из заголовков
        put_data = self.rfile.read(content_length)  # Читаем данные из запроса
        self._send_response(200, f'PUT request processed with data: {put_data.decode("utf-8")}')  # Отправляем успешный ответ

# Метод для обработки PUT-запросов
    def do_DELETE(self):
        if not self.authenticate():  # Проверяем авторизацию
            return  # Если авторизация не прошла, выходим из метода
        self._send_response(200, 'DELETE request processed')  # Отправляем успешный ответ

# Метод для аутентификации пользователя
    def authenticate(self):
        # Считываем заголовок авторизации
        auth_header = self.headers.get('Authorization')
        # Проверяем наличие заголовка авторизации
        if not auth_header:
            # Если заголовок отсутствует, отправляем ответ 401 (не авторизован)
            self.send_response(401)
            # Устанавливаем заголовок 'WWW-Authenticate', который сообщает клиенту, что требуется аутентификация.
            # В данном случае используется базовая аутентификация (Basic) с указанием "realm", который представляет собой область, защищенную аутентификацией.
            self.send_header('WWW-Authenticate', 'Basic realm="My Realm"')
            # Закрываем заголовки HTTP-ответа.
            self.end_headers()
            # Отправляем сообщение клиенту, информируя его о том, что для доступа к ресурсу требуется авторизация.
            self.wfile.write(b'Authorization required')
            # Возвращаем False
            return False

        # Разделяем тип аутентификации и информацию
        auth_type, auth_info = auth_header.split(' ', 1)
        # Проверяем, что тип аутентификации - Basic
        if auth_type.lower() != 'basic':
            # Если тип не Basic, отправляем ответ 401
            self.send_response(401)
            # Закрываем заголовки HTTP-ответа.
            self.end_headers()
            # Возвращаем False
            return False

        # Считываем информацию об авторизации из base64
        username, password = base64.b64decode(auth_info).decode('utf-8').split(':', 1)
        # Сравниваем полученные имя пользователя и пароль с заранее заданными
        if username == self.USERNAME and password == self.PASSWORD:
            # Если аутентификация успешна, возвращаем True
            return True
        else:
            # Если аутентификация не удалась, отправляем ответ 403 (доступ запрещен)
            self.send_response(403)
            # Закрываем заголовки HTTP-ответа.
            self.end_headers()
            # Отправляем клиенту HTTP - ответ с сообщением "Forbidden"(Запрещено).
            self.wfile.write(b'Forbidden')
            # Возвращаем False
            return False


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    # Создаем TCP-сервер, который будет обрабатывать запросы
    print(f"Serving on port {PORT}")
    # Запускаем сервер в бесконечном цикле
    httpd.serve_forever()