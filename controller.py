from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from io import BytesIO
from urls import Url
from views import View


class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        method = Url(self.path).get_method()
        if method:
            result, fields = method[0], method[1]
            json_result = View(result).to_json(fields)
            self.wfile.write(json_result.encode())


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())



