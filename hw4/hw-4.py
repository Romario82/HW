from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
import json
from datetime import datetime
import threading

UDP_IP = '127.0.0.1'
UDP_PORT1 = 3000
UDP_PORT2 = 5000
J_DATA = {}

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = '127.0.0.1', 5000
        sock.sendto(data, server)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def data_send(self, data):
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)

def run_web_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('127.0.0.1', UDP_PORT1)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
#-----------------Socket server---------------------------------
def json_f(data):
    data_time = str(datetime.now())
    J_DATA[data_time] = data
    print(data)
    with open('storage/data.json', 'w') as f:
        json.dump(J_DATA, f, indent=2)

def run_socket_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            data_parse = data.decode()
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            json_f(data_dict)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


if __name__ == '__main__':
    streams1 = threading.Thread(target=run_web_server, args=(), daemon=True)
    streams2 = threading.Thread(target=run_socket_server, args=(UDP_IP, UDP_PORT2), daemon=True)
    streams1.start()
    streams2.start()
    streams1.join()
    streams2.join()


