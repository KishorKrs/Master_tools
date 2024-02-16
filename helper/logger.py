import os
import logging
from colorlog import ColoredFormatter


class Log:
    def __init__(self, fpath, futil):
        self.logger = logging.getLogger("Logging")
        self.logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        self.logger.addHandler(sh)
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        formatter = ColoredFormatter(LOGFORMAT)
        sh.setFormatter(formatter)

        futil.make_dir(os.path.dirname(fpath))
        fh = logging.FileHandler(fpath)
        self.logger.addHandler(fh)
        fh.setFormatter(formatter)

    def info(self, log_text):
        self.logger.info(log_text)

    def error(self, log_text):
        self.logger.error(log_text)

    def critical(self, log_text):
        self.logger.critical(log_text)

    def warning(self, log_text):
        self.logger.warning(log_text)

    def debug(self, log_text):
        self.logger.debug(log_text)


if __name__ == "__main__":
    from config import Config
    from fileutil import Fileutil

    config = Config()
    fileutil = Fileutil()

    test_log = Fileutil().path_join(config.log_dir, "00_test", "test.log")
    log = Log(test_log, fileutil)
    log.info("This is INFO log")
    log.debug("This is DEBUG log")
    log.warning("This is WARNING log")
    log.error("This is ERROR log")
    log.critical("This is CRITICAL log")
