import json
import os
from typing import Type

import yaml


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
                with open(config_path, mode='r', encoding='utf-8') as config_file:
                    if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                        return yaml.safe_load(config_file), config_path
                    if config_path.endswith('.json'):
                        return json.load(config_file), config_path
                    if config_path.endswith('.py'):
                        return eval(config_file.read()), config_path
                    raise ValueError(f"Unsupported config file format: {config_path}")
        # Optionally, return a default configuration or raise an exception if no file is found.
        raise FileNotFoundError(f"None found: {config_paths}")

    @staticmethod
    def load_and_embed(*config_paths) -> (any, str):
        config, config_path = ConfigUtil.load(*config_paths)
        config_dir = os.path.dirname(config_path)
        ret = ConfigUtil.embed(config, config_dir)
        return ret, config_path

    @staticmethod
    def embed(data: (dict, list, tuple), base_path='') -> any:
        """
        Recursively iterates through all string values in a dictionary or list.
        If a string value starts with '#__file__#:', it treats the rest of the string as a file path,
        loads the content of the file, and embeds it back into the original dictionary or list.

        :param data: The dictionary or list to process.
        :param base_path: The base path to resolve relative file paths.
        """

        if data is None:
            return None

        cmd = '#__file__#:'
        cmd_len = len(cmd)

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and value.startswith(cmd):
                    file_name = value[cmd_len:]
                    file_path = os.path.join(base_path, file_name)
                    data[key], _ = ConfigUtil.load_and_embed(file_path)
                else:
                    ConfigUtil.embed(value, base_path)
            return data

        if isinstance(data, (list, tuple)):
            for i, item in enumerate(data):
                if isinstance(item, str) and item.startswith(cmd):
                    file_name = item[cmd_len:]
                    file_path = os.path.join(base_path, file_name)
                    data[i], _ = ConfigUtil.load_and_embed(file_path)
                else:
                    ConfigUtil.embed(item, base_path)
            return data

        return data

    @staticmethod
    def store(key: str, data: any) -> Type['ConfigUtil']:
        ConfigUtil._storage[key] = data
        return ConfigUtil

    @staticmethod
    def retrieve(key: str) -> any:
        return ConfigUtil._storage.get(key, None)
