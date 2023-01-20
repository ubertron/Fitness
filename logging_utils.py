import logging
import sys


class LoggingFormatter(logging.Formatter):
    error_format = "ERROR: %(msg)s"
    debug_format = "DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_format = "%(msg)s"

    def __init__(self, fmt: str = "%(levelno)s: %(msg)s", short: bool = True):
        logging.Formatter.__init__(self, "%(msg)s" if short else fmt)

    def format(self, record):
        format_orig = self._fmt

        if record.levelno == logging.DEBUG:
            self._fmt = LoggingFormatter.debug_format

        elif record.levelno == logging.INFO:
            self._fmt = LoggingFormatter.info_format

        elif record.levelno == logging.ERROR:
            self._fmt = LoggingFormatter.error_format

        result = logging.Formatter.format(self, record)
        self._fmt = format_orig

        return result


logging_format = LoggingFormatter()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging_format)
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
