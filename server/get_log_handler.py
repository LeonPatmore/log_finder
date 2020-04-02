import json

from logger.logger import logger
from server.handler import Handler
from server.server import UnknownLogFileException


class _BadPathException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class _TooManyCustomFieldsException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class GetLogHandler(Handler):

    def do_GET(self):
        try:
            path, query_params = self.clean_path()
            path_elements = path.split('/')

            # Ensure path has two elements.
            if len(path_elements) != 2:
                raise _BadPathException()

            log_name = path_elements[0]
            field_value = path_elements[-1]
            search_field = self.get_custom_search_field_or_none(query_params)

            if search_field is not None:
                logger.info("Searching for log [ {} ] using custom field [ {} ]".format(log_name, search_field))
                logs = self.get_server().get_json_by_query_field(log_name, search_field, field_value)

            else:
                logger.info("Searching for log [ {} ] using indexed field!".format(log_name))
                logs = self.get_server().get_json_by_id(log_name, field_value)

            self.send_response(202)
            self.send_header(Handler.CONTENT_TYPE_HEADER, Handler.CONTENT_TYPE_JSON)
            self.end_headers()
            self.wfile.write(json.dumps(logs).encode('utf-8'))
        except _BadPathException:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Bad path!".encode('utf-8'))
        except _TooManyCustomFieldsException:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("You must only provide one custom field param!".encode('utf-8'))
        except UnknownLogFileException:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Unknown log name!".encode('utf-8'))

    @staticmethod
    def get_custom_search_field_or_none(query_params: dict) -> str or None:
        """
        Gets the custom search field if provided, or will return none.
        """
        if "field" in query_params.keys():
            values = query_params.get("field")
            if len(values) > 1:
                raise _TooManyCustomFieldsException()
            return values[0]
        return None
