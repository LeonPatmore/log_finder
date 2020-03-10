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

            path = self.clean_path()
            path_elements = path.split('/')
            log_name = path_elements[0]
            field_value = path_elements[-1]

            if "trace_id" in path:
                logger.info("Searching for log [ {} ] with trace ID [ {} ]".format(log_name, field_value))
                logs = self.get_server().get_json_by_query_field(log_name, "traceId", field_value)

            else:
                logger.info("Searching for log [ {} ] with ID [ {} ]".format(log_name, field_value))
                logs = self.get_server().get_json_by_id(log_name, field_value)

            self.send_response(202)
            self.send_header(Handler.CONTENT_TYPE_HEADER, Handler.CONTENT_TYPE_JSON)
            self.end_headers()
            self.wfile.write(json.dumps(logs).encode('utf-8'))
        except _BadPathException:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Bad path!".encode('utf-8'))
        except UnknownLogFileException:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Unknown log name!".encode('utf-8'))

