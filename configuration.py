from . import logging

POSTGRESQL = {
    "database": "minpriroda",
    "user": "minpriroda",

}

ACCESS_DB = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\User\\Desktop\\ЕБДСОЗ (2019).accdb;'
log_config = {
    "version": 1,
    "root": {
        "handlers": ["console", "file", 'errors_file'],
        "level": "DEBUG",
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "filters": ["debugs"]
        },
        "file": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "migration_errors.log",
            "filters": ["info_&_warnings"]
        }
        ,
        "errors_file": {
            "formatter": "migration_error",
            "class": "logging.FileHandler",
            "level": "WARNING",
            "filename": "errors.log"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(message)s"
        },
        "migration_error": {
            "format": "%(name)s : %(funcName)s : %(message)s"
        }
    },
    "filters": {
        "info_&_warnings": {
            "()": logging.InfoAnWarningsOnly
        },
        'debugs': {
            "()": logging.ExcludeInfo
        }

    }

}
