import logging


class InfoAnWarningsOnly(logging.Filter):
    def filter(self, record):
        if 10 < record.levelno < 31:
            if record.levelno == 30:  # Updating Warning messages to Error.
                record.levelno = 40
                record.msg = "Error : " + record.msg
            return True
        else:
            return False


class ExcludeInfo(logging.Filter):
    def filter(self, record):
        if 10 < record.levelno < 21:
            return False
        return True
