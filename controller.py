from http.server import BaseHTTPRequestHandler
from error import Error
from urls import Url
from views import View


class HttpGetHandler(BaseHTTPRequestHandler):

    """Обработчик"""

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PATCH')
        self.send_header("Access-Control-Allow-Headers", "Content-type")
        self.end_headers()

    def do_GET(self):
        self.get_response()

    def do_POST(self):
        self.get_response()

    def do_PATCH(self):
        self.get_response()

    def get_response(self):
        if self.command in ('POST', 'PATCH'):
            data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        else:
            data = None
        response = Url(self.path, self.command).choose_dao(data=data)
        if isinstance(response, Error):
            self.send_response(response.code)
        else:
            code = 200 if self.command in ('GET', 'PATCH') else 201
            self.send_response(code)
        self.send_header('Content-type', 'text/json')
        self.send_header(keyword="Access-Control-Allow-Origin", value='*')
        self.send_header(keyword="Access-Control-Allow-Methods", value='GET, POST, PATCH, OPTIONS')
        self.send_header(keyword='Access-Control-Allow-Headers', value='Content-Type')
        self.end_headers()
        json_result = View(response).to_json()
        self.wfile.write(json_result.encode())



    # def do_GET(self):
    #     response = Url(self.path).router_for_get()
    #     if isinstance(response, ErrorResponse):
    #         self.send_response(response.code)
    #     else:
    #         self.send_response(200)
    #     self.send_header('Content-type', 'text/json')
    #     self.send_header(keyword="Access-Control-Allow-Origin", value='*')
    #     self.send_header(keyword="Access-Control-Allow-Methods", value='GET')
    #     self.send_header(keyword='Access-Control-Allow-Headers', value='Content-Type')
    #     self.end_headers()
    #     json_result = View(response).to_json()
    #     self.wfile.write(json_result.encode())
    #
    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])
    #     data = self.rfile.read(content_length).decode('utf-8')
    #     response = Url(self.path).router_for_post(data)
    #     self.send_response(201)
    #     self.send_header('Content-type', 'text/json')
    #     self.send_header(keyword="Access-Control-Allow-Origin", value='*')
    #     self.send_header(keyword="Access-Control-Allow-Methods", value='POST')
    #     self.send_header(keyword='Access-Control-Allow-Headers', value='Content-Type')
    #     self.end_headers()
    #     json_result = View(response).to_json()
    #     self.wfile.write(json_result.encode())
    #
    # def do_PATCH(self):
    #     data = self.rfile.read().decode('utf-8')
    #     response = Url(self.path).router_for_patch(data)
    #     self.send_response(200)
    #     self.send_header('Content-type', 'text/json')
    #     self.end_headers()
    #     json_result = View(response).to_json()
    #     self.wfile.write(json_result.encode())






