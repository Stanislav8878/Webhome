from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

# Определяем пути
BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
CSS_DIR = os.path.join(BASE_DIR, 'css')


class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""

        # Карта маршрутов
        routes = {
            '/': 'index.html',
            '/catalog': 'catalog.html',
            '/category': 'category.html',
            '/contacts': 'contacts.html'
        }

        # Отдача статических файлов Bootstrap (CSS / JS)
        if self.path.startswith('/css/'):
            file_path = os.path.join(BASE_DIR, self.path.lstrip('/'))

            if os.path.exists(file_path):
                self.send_response(200)

                # Определяем тип содержимого
                if file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css; charset=utf-8')
                elif file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript; charset=utf-8')
                else:
                    self.send_header('Content-type', 'application/octet-stream')

                self.end_headers()

                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "CSS/JS файл не найден")
                return

        # Определяем какую страницу вернуть
        filename = routes.get(self.path, 'contacts.html')
        file_path = os.path.join(TEMPLATES_DIR, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, "Страница не найдена")

    def do_POST(self):
        """Обработка POST-запросов с формы (например, /contacts)"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        print("\n=== Получены данные из формы ===")
        for key, value in data.items():
            print(f"{key}: {value[0]}")
        print("================================\n")

        # Ответ пользователю
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        response = """
        <html lang='ru'>
        <head><meta charset='UTF-8'><title>Спасибо!</title></head>
        <body style='font-family: sans-serif; padding: 20px;'>
            <h3>Спасибо! Ваше сообщение получено.</h3>
            <a href='/contacts'>← Вернуться назад</a>
        </body>
        </html>
        """
        self.wfile.write(response.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHandler):
    """Запуск локального сервера"""
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("🚀 Сервер запущен на http://localhost:8080")
    print("Нажмите Ctrl+C для остановки.")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
