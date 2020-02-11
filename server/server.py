import threading
from http.server import HTTPServer
from time import sleep

from configuration.configuration import Configuration
from file_searcher.file_searcher import FileSearcher
from logger.logger import logger
from mongodb.mongo_client import MongoClient
from mongodb.mongo_database import MongoDatabase
from server.handler import Handler
from server.logs import generate_logs, Log


class UnknownLogFileException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class Server(HTTPServer):

    def __init__(self, configuration: Configuration, handler: Handler = None):
        super().__init__((configuration.get_property("server.host"),
                          configuration.get_property("server.port")),
                         handler)
        self.file_searcher = FileSearcher(True, False)
        self.running = False

        self.logs = generate_logs(configuration)

        mongo_database = MongoClient(configuration.get_property("mongo.host"),
                                     int(configuration.get_property("mongo.port"))) \
            .get_database(configuration.get_property("mongo.database"))

        self.collections = self._generate_collections(self.logs, mongo_database)

    def start(self):
        if self.running:
            raise SystemError("Can not start server since it is already running!")
        self.running = True
        threading.Thread(target=self._schedule_refresh_logs).start()
        self.serve_forever()

    def safe_insert(self, json: dict, log: Log):
        if log.index_field in json:
            self.collections.get(log.name).insert(json)

    def get_json_by_id(self, log_name: str, index_id: str) -> list:
        log = self._get_log_by_name(log_name)
        if log is None:
            raise UnknownLogFileException("Log name [ {} ] is not known!".format(log_name))
        return self.collections.get(log_name).query({log.index_field: index_id}, True)

    def _get_log_by_name(self, log_name: str) -> Log or None:
        for log in self.logs:
            if log.name == log_name:
                return log
        return None

    @staticmethod
    def _generate_collections(logs: list, mongo_database: MongoDatabase) -> dict:
        collections = dict()
        for log in logs:
            log_mongo_collection = mongo_database.get_collection(log.name)
            log_mongo_collection.create_index(log.index_field)
            collections.update({
                log.name: log_mongo_collection
            })
        return collections

    def _refresh_logs(self):
        for log in self.logs:
            files = self.file_searcher.get_files_by_regex(log.file_path)
            for file in files:
                jsons = self.file_searcher.file_to_jsons(file)
                for json in jsons:
                    self.safe_insert(json, log)

    def _schedule_refresh_logs(self):
        while self.running:
            logger.info("Running logs refresh!")
            self._refresh_logs()
            sleep(2)
