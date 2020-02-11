from configuration.configuration import Configuration
from logger.logger import logger


def generate_logs(configuration: Configuration) -> list:
    logs_string = configuration.get_property("logs")
    logger.info("Loading logs config [ {} ]".format(logs_string))
    logs = list()
    for log_string in logs_string.split(","):
        log_info = log_string.split(":")
        if len(log_info) != 3:
            raise Exception("Log config is not recognised!")
        logs.append(Log(*log_info))
    return logs


class Log(object):

    def __init__(self, name: str, file_path: str, index_field: str):
        self.name = name
        self.file_path = file_path
        self.index_field = index_field
