import os


class Config:
    def __init__(self) -> None:
        exec_dirname = "exec"
        helper_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(helper_dir)
        self.exec_dir = os.path.join(os.path.dirname(project_dir), exec_dirname)
        self.log_dir = os.path.join(self.exec_dir, "Logger")
        self.sample_dir = os.path.join(project_dir, "Sample_files")


if __name__ == "__main__":
    config = Config()
    pass
