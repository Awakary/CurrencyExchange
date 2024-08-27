from http.server import HTTPServer

from controller.controller import HttpGetHandler


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    """Функция запуска сервера"""

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
