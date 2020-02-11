import json

from logger.logger import logger
from server.handler import Handler
from server.server import UnknownLogFileException


class _BadPathException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class GetLogHandler(Handler):

    def do_GET(self):
        try:
            log_name, index_id = self._parse_path(self.clean_path())

            logger.info("Searching for log [ {} ] with ID [ {} ]".format(log_name, index_id))
            self.send_response(202)
            self.send_header(Handler.CONTENT_TYPE_HEADER, Handler.CONTENT_TYPE_JSON)
            self.end_headers()
            self.wfile.write(json.dumps(self.get_server().get_json_by_id(log_name, index_id)).encode('utf-8'))
        except _BadPathException:
            self.send_response(400)
            self.wfile.write("Bad path!".encode('utf-8'))
        except UnknownLogFileException:
            self.send_response(400)
            self.wfile.write("Unknown log name!".encode('utf-8'))

    @staticmethod
    def _parse_path(path: str) -> tuple:
        if path.startswith("/"):
            path = path[1:]
        path_elements = path.split('/')
        if len(path_elements) != 2:
            raise _BadPathException("Path [ {} ] does not have two elements!".format(path))
        return path_elements[0], path_elements[1]
