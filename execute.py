from . import base_models, manage

"""
Файл с описанием всех моделей для миграции

Ошибки связанные с отсутсвием справочной информации будут выведены в файл migration_errors.log
Ошибки связанные с критическими ошибками будут выведены в файл errors.log


пример описания модели:
        class Organisation(Model):
        атрибуты(экземпляры классов Field):
            reporting_period = base_models.IntegerField(verbose_name='год')
            название колонки в postgresql = ...Field(**kwargs)

        access_db_table = Название таблицы в ms access
        postgre_db_table = Название таблицы в postgresql
"""


# class Organisation(base_models.Model):
#     id = base_models.IntegerField(verbose_name='Код_ЮЛ')
#     name = base_models.CharField(verbose_name='Предприятие')
#     okogu_id = base_models.ManualField(verbose_name='Министерство', table_name_in_postgre_db='okogu',
#                                        fields_to_look_up=['name', 'short_name'])
#     address_post = base_models.CharField(verbose_name='Адрес')
#     address_region_id = base_models.ManualField(verbose_name='Область', table_name_in_postgre_db='region',
#                                                 fields_to_look_up=['code'])
#     address_district_id = base_models.ManualField(verbose_name='Район', table_name_in_postgre_db='district',
#                                                   fields_to_look_up=['code'])
#     address_locale_id = base_models.ManualField(verbose_name='YG', table_name_in_postgre_db='locale',
#                                                 fields_to_look_up=['name'], parse=True, position=2)
#     okpo = base_models.CharField(verbose_name='ОКПО')
#     unp = base_models.CharField(verbose_name='ОКЮЛП')
#     okad_id = base_models.ManualField(verbose_name='ОКЭД', table_name_in_postgre_db='okad', fields_to_look_up=['code'])
#     soato = base_models.CharField(verbose_name='СОАТО')
#     okfs_id = base_models.ManualField(verbose_name='ОКФС', table_name_in_postgre_db='okfs', fields_to_look_up=['code'])
#     okopf_id = base_models.ManualField(verbose_name='ОКОПФ', table_name_in_postgre_db='okopf',
#                                        fields_to_look_up=['code'])
#     short_name = base_models.CharField(verbose_name='Предприятие')
#     company_main_id = base_models.ManualField(verbose_name='Министерство', table_name_in_postgre_db='company',
#                                               fields_to_look_up=['name', 'short_name'])
#     is_active = base_models.DefaultField(default=True)
#
#     access_db_table = 'Справочник_предприятий'
#     postgre_db_table = 'Company'
#
#
# class DepositedPesticideForm(base_models.Model):
#     reporting_period = base_models.IntegerField(verbose_name='год')
#     organisation_id = base_models.ManualField(verbose_name='код_предприятия', table_name_in_postgre_db='company',
#                                               fields_to_look_up=['id'])
#     pesticide_id = base_models.ManualField(verbose_name='наименование_пестицида', table_name_in_postgre_db='pesticide',
#                                            fields_to_look_up=['name'])
#     physical_state_id = base_models.ManualField(verbose_name='агрегатное_состояние',
#                                                 table_name_in_postgre_db='physical_state', fields_to_look_up=['code'])
#     qty = base_models.DecimalField(verbose_name='всего')
#     from_graves = base_models.DefaultField(default=0.0)
#     is_active = base_models.DefaultField(default=True)
#     access_db_table = 'КУП'
#     postgre_db_table = 'deposited_pesticide_form'


models = []
# models = [Organisation, DepositedPesticideForm]

if __name__ == '__main__':
    manage.migrate(models)
