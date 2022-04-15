import logging


class ManualError(Exception):
    """Исключение вызывается когда не найдена запись справочника в postgresql"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        super(ManualError, self).__init__()


# f'Не найдена запись в {exc.table_name}|{values[i]}'
class CustomSingleTon:
    """Удаляет предыдущий экземпляр при создании нового"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            del cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance


class ManualMigrationError(CustomSingleTon):
    """Класс для отображения ненайденных записей в справочниках postgresql"""
    def __init__(self, values):
        self.values = values
        self.errors = {}

    def add_error(self, manual_table_name: str, value):
        self.errors[manual_table_name] = value

    def logging(self):
        if self.errors:
            logging_text = f'{self.values}| '
            for table_name, value in self.errors.items():
                logging_text += f'{table_name} - {value}; '
            logging.info(logging_text)

