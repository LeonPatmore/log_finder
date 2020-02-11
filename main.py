from configuration.configuration import Configuration
from server.get_log_handler import GetLogHandler
from server.server import Server


def start():
    configuration = Configuration("application.yaml")
    server = Server(configuration, GetLogHandler)
    server.start()


if __name__ == "__main__":
    start()
