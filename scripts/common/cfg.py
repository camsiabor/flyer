import os
from typing import Type

from scripts.common.directive import Directorate
from scripts.common.fileutil import FileUtil


class ConfigUtil:
    _storage = {}

    @staticmethod
    def load(*config_paths) -> (any, str):
        """
        Load the first existing configuration file from the given paths.
        :param config_paths: Variable number of paths to configuration files.
        :return: The loaded configuration as a dictionary.
        """
        for config_path in config_paths:
            if os.path.exists(config_path):
                return FileUtil.load(config_path), config_path
        # Optionally, return a default configuration or raise an exception if no file is found.
        raise FileNotFoundError(f"None found: {config_paths}")

    @staticmethod
    def load_and_embed(*config_paths) -> (any, str):
        config, config_path = ConfigUtil.load(*config_paths)
        ret = Directorate.embed(config)
        return ret, config_path

    @staticmethod
    def store(key: str, data: any) -> Type['ConfigUtil']:
        ConfigUtil._storage[key] = data
        return ConfigUtil

    @staticmethod
    def retrieve(key: str) -> any:
        return ConfigUtil._storage.get(key, None)
