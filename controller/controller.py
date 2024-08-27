from http.server import BaseHTTPRequestHandler

from controller.urls import Router
from utils.error import Error
from views import View


class HttpGetHandler(BaseHTTPRequestHandler):

    """Класс контроллера"""

    def do_OPTIONS(self):
        self.send_response(200)
        self.get_headers()

    def do_GET(self):
        self.get_response()

    def do_POST(self):
        self.get_response()

    def do_PATCH(self):
        self.get_response()

    def get_response(self):

        """Функция формирования ответа"""

        if self.command in ('POST', 'PATCH'):
            data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        else:
            data = None
        response = Router(path=self.path, method=self.command, data=data).get_router()
        if isinstance(response, Error):
            self.send_response(response.code)
        else:
            code = 200 if self.command in ('GET', 'PATCH') else 201
            self.send_response(code)
        self.get_headers()
        json_result = View(response).to_json()
        self.wfile.write(json_result.encode())

    def get_headers(self):

        """Функция отправки заголовков"""

        self.send_header('Content-type', 'text/json')
        self.send_header(keyword="Access-Control-Allow-Origin", value='*')
        self.send_header(keyword="Access-Control-Allow-Methods", value='GET, POST, PATCH, OPTIONS')
        self.send_header(keyword='Access-Control-Allow-Headers', value='Content-Type')
        self.end_headers()





