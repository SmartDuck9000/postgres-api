from flask import Flask, request, jsonify

import os
from dotenv import load_dotenv
from termcolor import colored

from postgres import Postgres
from psycopg2 import sql

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
        self.__select = self.app.route('/api/select', methods=['GET'])(self.__select)
        self.__select__with_join = self.app.route('/api/select_with_join', methods=['GET'])(self.__select__with_join)
        self.__insert = self.app.route('/api/insert', methods=['POST'])(self.__insert)
        self.__update = self.app.route('/api/update', methods=['POST'])(self.__update)

    def __select(self):
        data = request.json
        ordered_field = None
        sql_conditions = None

        try:
            table = data['table']
            fields = data['fields']
        except Exception as e:
            print(colored(e, color='red'))
            return jsonify({
                "error": e,
                "code": 400
            })

        if 'ordered_field' in data:
            ordered_field = data['ordered_field']
        if 'conditions' in data:
            sql_conditions = self.__parse_conditions(data['conditions'])

        res = self.db.select(table, fields, ordered_field, sql_conditions)
        return jsonify(res)

    def __select__with_join(self):
        data = request.json
        ordered_field = None
        sql_conditions = None

        try:
            join_tables = data['join_tables']
            join_fields = data['join_fields']
            fields = data['fields']
        except Exception as e:
            print(colored(e, color='red'))
            return jsonify({
                "error": e,
                "code": 400
            })

        if 'ordered_field' in data:
            ordered_field = data['ordered_field']
        if 'conditions' in data:
            sql_conditions = self.__parse_conditions(data['conditions'])

        try:
            res = self.db.select_with_join(join_tables, join_fields, fields, ordered_field, sql_conditions)
        except Exception as e:
            print(colored(e, color='red'))
            return jsonify({
                "error": e,
                "code": 400
            })

        return jsonify(res)

    def __insert(self):
        data = request.json

        try:
            table = data['table']
            values = data['values']
        except Exception as e:
            print(colored(e, color='red'))
            return jsonify({
                "error": e,
                "code": 400
            })

        res = self.db.insert(table, values)
        return jsonify(res)

    def __update(self):
        pass

    def __parse_conditions(self, conditions):
        if conditions is None:
            return None
        sql_conditions = []

        for entity in conditions:
            for field in conditions[entity]:
                if type(conditions[entity][field]) == dict:
                    from_value = str(conditions[entity][field]['from'])
                    to_value = str(conditions[entity][field]['to'])
                    sql_condition = sql.Identifier(field) + sql.SQL(' BETWEEN ') + sql.SQL(from_value) + sql.SQL(' AND ') + sql.SQL(to_value)
                else:
                    val = str(conditions[entity][field])

                    table_field = field.split('.')
                    if len(table_field) == 2:
                        field = sql.SQL(table_field[0] + '.') + sql.Identifier(table_field[1])
                    else:
                        field = sql.Identifier(field)

                    sql_condition = field + sql.SQL(' = ') + sql.SQL(val)
                sql_conditions.append(sql_condition)

        if not sql_conditions:
            sql_conditions = None

        return sql_conditions


if __name__ == '__main__':
    server = DatabaseServer()
    server.run()
