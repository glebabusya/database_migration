from .exceptions import ManualError, ManualMigrationError


class ModelBase(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(mcs, name, bases, attrs)
        new_class = super_new(mcs, name, bases, attrs)
        fields = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Field):
                fields[obj_name] = obj
        new_class.fields = fields
        return new_class


class Field:
    def __init__(self, verbose_name: str):
        self.verbose_name = verbose_name

    def __str__(self):
        return self.verbose_name

    def add_value(self, value):
        if value:
            self.value = value
        else:
            self.value = 'NULL'
        return self


class IntegerField(Field):
    pass


class CharField(Field):
    def add_value(self, value):
        if value:
            self.value = f"'{value}'"
        else:
            self.value = 'NULL'
        return self


class BooleanField(Field):
    pass


class DecimalField(Field):
    pass


class DefaultField(Field):
    def __init__(self, default):
        self.value = default

    def __str__(self):
        return str(self.value)


class ManualField(Field):
    def __init__(self, verbose_name: str, table_name_in_postgre_db: str, fields_to_look_up: list, parse: bool = False,
                 position: int = None, delimiter: str = ' '):
        """
        verbose_name: название колонки в аксес
        table_name_in_postgre_db: название таблицы в постгре
        fields_to_look_up: список полей по которым нужно проводить поиск в постгре
        parse: True/False Нужно ли парсить поле из аксеса
        position: Если parse=True. Число, показывающее какой порядковый в списке распаршенных данных брать для поиска (начинается с 1)
        delimiter: Символ по которому парсить поле из аксеса
        """
        if parse != bool(position):
            raise AttributeError('"parse" и "position" дожны быть заданы вместе, %s' % verbose_name)
        super(ManualField, self).__init__(verbose_name)
        self.fields_to_look_up = fields_to_look_up
        self.table_name_in_postgre_db = table_name_in_postgre_db
        self.parse = parse
        self.parsed_position = position
        self.delimiter = delimiter

    def find_manual_in_postgre_db(self, value, cursor=None):
        if not value:
            self.value = 'null'
            return self
        if self.parse:
            value = value.split(self.delimiter)[self.parsed_position - 1]

        query = f'''SELECT id from {self.table_name_in_postgre_db} where'''
        for field in self.fields_to_look_up:

            if 'name' == field:
                query += f''' "{field}" IN ('{value}') OR'''
            elif 'id' in field:
                query += f''' "{field}" = {value} OR'''
            else:
                query += f''' {field} ILIKE '{value}' OR'''
        query = query[:-2]
        cursor.execute(query)
        try:
            pk = cursor.fetchall()[0][0]
            self.value = pk
        except IndexError:
            self.value = 'null'
            raise ManualError(table_name=self.table_name_in_postgre_db)
        return self.value


class Model(metaclass=ModelBase):
    @classmethod
    def manage_fields(cls, values, cursor=None):
        errors = ManualMigrationError(values)
        fields = list(cls.fields.values())
        for i in range(len(values)):
            field = fields[i]
            if isinstance(field, ManualField):
                try:
                    field.find_manual_in_postgre_db(values[i], cursor)
                except ManualError as exc:
                    errors.add_error(exc.table_name, values[i])
            elif not isinstance(field, DefaultField):
                field.add_value(values[i])
        errors.logging()

    @classmethod
    def get_query_to_access(cls):
        fields = cls.fields
        string = """SELECT"""
        for field_alter_name, field in fields.items():
            if not isinstance(field, DefaultField):
                string += f' {field},'
        string = string[:-1]
        string += f' from {cls.access_db_table} '
        return string

    @classmethod
    def get_query_to_postgre(cls):
        fields = cls.fields
        first_part_query = f'INSERT INTO {cls.postgre_db_table} ('
        second_part_query = ' VALUES ('
        for field_name, field in fields.items():
            first_part_query += f' {field_name}, '
            second_part_query += f' {field.value}, '

        result_query = first_part_query[:-2] + ')' + second_part_query[:-2] + ')'
        return result_query
