from . import configuration
from .db_connection import DatabasesConnection
import logging
from logging import config


def migrate(models: list):
    config.dictConfig(configuration.log_config)
    with DatabasesConnection(postgre_data=configuration.POSTGRESQL, access_data=configuration.ACCESS_DB) as connections:
        postgre_connection, access_connection = connections
        access_cursor = access_connection.cursor()
        postgre_cursor = postgre_connection.cursor()
        for model in models:
            access_cursor.execute(model.get_query_to_access())
            i = 0
            for raw in access_cursor.fetchall():
                i += 1
                if i == 11:
                    break
                try:
                    model.manage_fields(raw, cursor=postgre_cursor)
                    query = model.get_query_to_postgre()
                    postgre_cursor.execute(query)
                    postgre_connection.commit()
                    logging.debug('Запись загружена')
                except Exception as e:
                    logging.error(e.args)

    logging.debug('Миграция завершена')
