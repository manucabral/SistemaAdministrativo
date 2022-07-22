import os
import pickle


class Directory:

    def __init__(self, app_name: str, file_extension: str):
        self.file_extension = file_extension
        self.app_name = app_name

    @property
    def roaming_path(self) -> str:
        return os.getenv('APPDATA')

    @property
    def app_path(self) -> str:
        return f'{self.roaming_path}\\{self.app_name}'

    def create(self) -> None:
        if not os.path.exists(self.app_path):
            os.mkdir(self.app_path)

    def full_path(self, filename: str) -> str:
        return f'{self.app_path}\\{filename}.{self.file_extension}'

    def file_exists(self, filename: str) -> bool:
        try:
            with open(self.full_path(filename), 'rb') as file:
                return True
        except FileNotFoundError:
            return False

    def save_file(self, filename: str, data: object) -> bool:
        try:
            with open(self.full_path(filename), 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(e)
            return False

    def load_file(self, filename: str) -> object:
        try:
            with open(self.full_path(filename), 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(e)
            return []
