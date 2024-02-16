from datetime import datetime as dt

# helper modules
from helper.logger import Log
from helper.config import Config
from helper.fileutil import Fileutil


class Main:
    def __init__(self, app_name) -> None:
        self.app_name = app_name
        self.start_dt = dt.now().strftime("%Y-%m-%d_%H%M%S")

        self.config = Config()
        self.futil = Fileutil()
        logger_fpath = self.futil.path_join(self.config.log_dir, self.app_name, self.start_dt + ".log")
        self.log = Log(logger_fpath, self.futil)

    def exec_main(self):
        self.log.warning("Implement your own exec_main() Method!!!")


if __name__ == "__main__":
    main = Main("test_main")
    main.exec_main()
