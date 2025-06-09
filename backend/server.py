#!/usr/bin/env python3
"""Simple backend server accepting configuration via POST /configuration."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class ConfigHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != '/configuration':
            self.send_error(404, 'Not Found')
            return
        content_length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(content_length)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')
            return
        print('Received configuration:', data, flush=True)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "received"}')


def run_server(ip: str = '127.0.0.1', port: int = 8000) -> None:
    """Run HTTP server on provided IP and port."""
    httpd = HTTPServer((ip, port), ConfigHandler)
    print(f'Server listening on {ip}:{port}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simple backend configuration server')
    parser.add_argument('--ip', default='127.0.0.1', help='IP address to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    args = parser.parse_args()
    run_server(args.ip, args.port)
