from flask import Flask, request

import os
from dotenv import load_dotenv

from postgres import Postgres

class DatabaseServer:

    def __init__(self, config_file='.env'):
        self.app = Flask(__name__)

        try:
            dotenv_path = os.path.join(os.path.dirname(__file__), config_file)
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path)

            self.host = os.environ.get('server_host')
            self.port = os.environ.get('server_port')

            self.db = Postgres(
                db_name=os.environ.get('db_name'),
                db_username=os.environ.get('db_username'),
                db_password=os.environ.get('db_password'),
                db_host=os.environ.get('db_host'),
                db_port=os.environ.get('db_port'),
                log_file=os.environ.get('log_file')
            )
        except Exception as e:
            print(e)

        self.__setup_routes()

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def __setup_routes(self):
        self.__select = self.app.route('/api/select')(self.__select)

    def __select(self):
        data = request.json


if __name__ == '__main__':
    server = DatabaseServer()
    server.run()
