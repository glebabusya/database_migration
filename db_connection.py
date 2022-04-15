import psycopg2
import pyodbc


class DatabasesConnection:
    def __init__(self, postgre_data, access_data):
        self._postgre_data = postgre_data
        self._access_data = access_data

    def __enter__(self):
        self.postgre_connection = psycopg2.connect(**self._postgre_data)
        self.access_connection = pyodbc.connect(self._access_data)
        return self.postgre_connection, self.access_connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.postgre_connection.close()
        self.access_connection.close()
