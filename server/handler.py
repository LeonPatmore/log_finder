from http.server import BaseHTTPRequestHandler
from urllib import parse


class Handler(BaseHTTPRequestHandler):

    CONTENT_TYPE_HEADER = "Content-Type"
    CONTENT_TYPE_JSON = "application/json"

    def do_GET(self):
        return self.send_error(403)

    def do_POST(self) :
        return self.send_error(403)

    def get_server(self):
        return self.server

    def clean_path(self) -> str:
        url_parse = parse.urlparse(self.path)
        query_params = parse.parse_qs(url_parse.query)
        path = url_parse.path  # type: str
        if path.startswith("/"):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return path, query_params
