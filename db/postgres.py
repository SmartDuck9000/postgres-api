import psycopg2
from psycopg2 import sql, extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import os
from dotenv import load_dotenv

from termcolor import colored

class Postgres:

    def __init__(self, db_name, db_username, db_password, db_host, db_port):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        try:
            self._connection = psycopg2.connect(dbname=db_name,
                                                user=db_username,
                                                password=db_password,
                                                host=db_host,
                                                port=db_port)
            self._connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self._cursor = self._connection.cursor(cursor_factory=extras.DictCursor)
        except Exception as e:
            print(colored(e, color='red'))
            return

        print(colored('Connect to postgres server: ' + db_host + ':' + db_port, color='green'))

    def __execute(self, query, commit=False, fetch=True):
        try:
            self._cursor.execute(query)
            if commit:
                self._connection.commit()
            if fetch:
                return [{key: value for key, value in row.items()} for row in self._cursor]
        except Exception as e:
            print(colored(e, color='red'))
