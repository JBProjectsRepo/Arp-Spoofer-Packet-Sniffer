from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import ssl


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Hello World!", "utf-8"))


def get_ssl_context(certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile, keyfile)
    context.set_ciphers("@SECLEVEL=1:ALL")
    return context


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


def serve_on_port(port):
    ip = "192.168.0.27"
    server = HTTPServer((ip, port), Handler)
    context = get_ssl_context("cert.pem", "key.pem")
    server.socket = context.wrap_socket(server.socket, server_side=True)
    server.serve_forever()


# def serve_on_port_v6(port):
#     server_v6 = HTTPServerV6(('::', port), Handler)
#     server_v6.serve_forever()


Thread(target=serve_on_port, args=[80]).start()
Thread(target=serve_on_port, args=[443]).start()
# Thread(target=serve_on_port_v6, args=[80]).start()
# Thread(target=serve_on_port_v6, args=[443]).start()
