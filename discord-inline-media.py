from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
import sys


class HTTPHandler(BaseHTTPRequestHandler):
    def send_code(self, code):
        self.send_response(code)
        self.send_header("Content-type", "text/plain;charset=UTF-8")
        self.end_headers()
        self.wfile.write(b"%d." % code)

    def send_file(self, resp):
        self.send_response(200)

        for header, value in resp.getheaders():
            if header == "Content-Disposition":
                self.send_header("Content-Disposition", "inline")
            else:
                self.send_header(header, value)

        self.end_headers()

        while True:
            pkt = resp.read(8192)

            if len(pkt) == 0:
                break

            self.wfile.write(pkt)

    def do_GET(self):
        try:
            if not self.path.startswith("/attachments"):
                self.send_code(404)
                return

            req = Request(
                f"https://media.discordapp.net{self.path}", headers={'User-Agent': 'Mozilla'}
            )

            resp = urlopen(req)
            self.send_file(resp)
        except Exception:
            self.send_code(403)


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <bindip> <port>\n" % sys.argv[0])
        sys.exit()

    ip = sys.argv[1]
    port = int(sys.argv[2])
    server = HTTPServer((ip, port), HTTPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


main()
