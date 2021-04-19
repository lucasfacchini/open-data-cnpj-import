import logging
import sys

from datetime import datetime
from logging.handlers import RotatingFileHandler

class Log:
    LOG_FILE_FORMAT = '%(asctime)s — %(levelname)s — %(message)s'
    LOG_FILE_MAX_SIZE = 10000000
    LOG_CONSOLE_FORMAT = '(%(levelname)s): %(message)s'
    LOG_FILE_DIR = 'logs/'

    def __init__(self):
        log_name = 'log' + datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        self.setup_file_handler(log_name)
        self.setup_console_handler()

    def setup_file_handler(self, log_name):
        file_handler = RotatingFileHandler(
            self.LOG_FILE_DIR + log_name + '.log',
            maxBytes=self.LOG_FILE_MAX_SIZE,
            backupCount=1
        )
        file_handler.setFormatter(logging.Formatter(self.LOG_FILE_FORMAT))
        self.logger.addHandler(file_handler)

    def setup_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(self.LOG_CONSOLE_FORMAT))
        self.logger.addHandler(console_handler)

    def debug(self, *messages):
        self._log(logging.DEBUG, messages)

    def info(self, *messages):
        self._log(logging.INFO, messages)

    def error(self, *messages):
        self._log(logging.ERROR, messages)

    def warn(self, *messages):
        self._log(logging.WARN, messages)

    def _log(self, level, messages):
        messages = list(map(lambda arg: str(arg), messages))
        message = ' '.join(messages)

        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.WARN:
            self.logger.warn(message)