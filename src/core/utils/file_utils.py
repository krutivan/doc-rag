import os

class FileUtils:
    @staticmethod
    def create_directories_if_not_exists(filepath: str) -> None:
        """
        Recursively create directories in a filepath if they do not exist.
        """
        dir_path = os.path.dirname(filepath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @staticmethod
    def get_filename(filepath: str) -> str:
        """
        Return the filename from a file path.
        """
        return os.path.basename(filepath)
