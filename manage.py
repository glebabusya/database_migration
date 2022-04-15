from . import configuration
from .db_connection import DatabasesConnection
import logging
from logging import config


def migrate(models: list):
    config.dictConfig(configuration.log_config)  # Подключение логирования
    with DatabasesConnection(postgre_data=configuration.POSTGRESQL,
                             access_data=configuration.ACCESS_DB) as connections:  # Открытие двух соединений с бд
        postgre_connection, access_connection = connections
        access_cursor = access_connection.cursor()
        postgre_cursor = postgre_connection.cursor()
        for model in models:
            access_cursor.execute(model.get_query_to_access())  # Выполнение запроса в ms access
            for raw in access_cursor.fetchall():  # Получение всех данных из таблицы ms access
                try:
                    model.manage_fields(raw, cursor=postgre_cursor)  # Форматирование данных
                    query = model.get_query_to_postgre()  # Получение запроса в postgresql
                    postgre_cursor.execute(query)  # Выполнение запроса
                    postgre_connection.commit()  # Сохранение изменений
                    logging.debug('Запись загружена')
                except Exception as e:
                    logging.error(e.args)

    logging.debug('Миграция завершена')
