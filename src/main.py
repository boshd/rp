# coding=utf8
import json, os

from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from proxy.proxy import Proxy

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path.startswith('/get'):
            value, exists, source = server.proxy.get(parsed_url)
            if exists:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                if value != None:
                    self.wfile.write(bytes("{\"value\": \"" + str(value.decode()) + "\", \"source\": \""+ str(source.decode()) + "\"}", 'utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes('key was not found', 'utf-8'))
        elif parsed_url.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('Proxy server running.', 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Resource not found', 'utf-8'))
        return

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len))
        k, v = post_body['k'], post_body['v']
        self.send_response(200)
        return server.proxy.put(k, v)

class Server(ThreadingMixIn, HTTPServer):
    def __init__(self, redis_host, redis_port, record_capacity, record_expiry, server_address, RequestHandlerClass, bind_and_activate = ...):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

        self.proxy = Proxy(redis_host, redis_port, record_capacity, record_expiry)

if __name__ == "__main__":
    host_name = os.getenv('HOST_NAME', 'localhost')
    server_port = os.getenv('SERVER_PORT', 8080)
    record_capacity = os.getenv('RECORD_CAPACITY', 5)
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = os.getenv('REDIS_PORT', 6379)
    record_expiry = os.getenv('RECORD_EXPIRY', 10)

    server = Server(redis_host, redis_port, record_capacity, record_expiry,(host_name, server_port), RequestHandler)

    print('starting server @ http://%s:%s' % (host_name, server_port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('keyboard interruption // server stopped')