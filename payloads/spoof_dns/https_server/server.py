from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        if self.path == '/':
            self.path = '/index.html'
        try:
            index_html = open(self.path[1:]).read()
            self.send_response(200)
        except:
            index_html = "File Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(index_html, "utf-8"))


def get_ssl_context(certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)
    context.set_ciphers("@SECLEVEL=1:ALL")
    return context


def serve_on_port(port, https):
    ip = "192.168.0.27"
    server = HTTPServer((ip, port), Handler)
    if https is True:
        context = get_ssl_context("cert.pem", "key.pem")
        server.socket = context.wrap_socket(server.socket, server_side=True)
    server.serve_forever()


Thread(target=serve_on_port, args=[80, False]).start()
Thread(target=serve_on_port, args=[443, True]).start()

# class HTTPServerV6(HTTPServer):
#     address_family = socket.AF_INET6

# def serve_on_port_v6(port):
#     server_v6 = HTTPServerV6(('::', port), Handler)
#     server_v6.serve_forever()

# Thread(target=serve_on_port_v6, args=[80]).start()
# Thread(target=serve_on_port_v6, args=[443]).start()

