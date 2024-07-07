import datetime
import functools
import json
import logging
import os
import time

import yaml

from scripts.common.serial import TypeList

# get / set / clone =============================================================================== #


VALUE_TYPES = (int, str, float, bool)
SERIAL_TYPES = (list, tuple, set)
PRIMITIVE_TYPES = (int, str, float, bool, list, tuple, set, dict)


def getv(cfg: dict, default=None, *keys):
    value = cfg
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
    if value is None:
        return default
    return value


def setv(target: dict, value, *keys):
    current = target
    paths = keys[:-1]
    for key in paths:
        if key in current and isinstance(current[key], dict):
            current = current[key]
        else:
            current[key] = {}
            current = current[key]
    last = keys[-1]
    current[last] = value
    return current


def clonev(src: dict, des: dict, default=None, *keys):
    if not keys:
        return

    current_src = src
    current_des = des

    paths = keys[:-1]
    for key in paths:
        if key in current_src and isinstance(current_src[key], dict):
            current_src = current_src[key]
            if key not in current_des:
                current_des[key] = {}
            current_des = current_des[key]
        else:
            return setv(current_des, default, *keys)

    last_key = keys[-1]
    if last_key in current_src:
        value = current_src[last_key]
        if value is not None:
            current_des[last_key] = value
        else:
            current_des[last_key] = default

    return current_des


# Reflection =============================================================================== #
class Reflector:

    @staticmethod
    def from_dict(obj: object, data: dict):
        for attr_name in dir(obj):
            if attr_name.startswith("__"):
                continue
            attr_value = getattr(obj, attr_name, None)
            if attr_name not in data:
                continue
            data_value = data[attr_name]

            if isinstance(attr_value, TypeList) and isinstance(data_value, SERIAL_TYPES):
                Reflector.from_serial(attr_value, data_value)
                continue

            if attr_value is None and isinstance(data_value, PRIMITIVE_TYPES):
                setattr(obj, attr_name, data_value)
                continue

            if isinstance(data_value, dict) and not isinstance(attr_value, PRIMITIVE_TYPES):
                # If the attribute is a complex type and the corresponding data is a dictionary,
                # recursively update or instantiate this attribute.
                if attr_value is None:
                    # If the attribute is None, try to instantiate it if it's a class.
                    attr_type = type(attr_value)
                    new_obj = attr_type() if attr_type not in PRIMITIVE_TYPES else data_value
                    setattr(obj, attr_name, Reflector.from_dict(new_obj, data_value))
                else:
                    # If the attribute already has a value, update it recursively.
                    setattr(obj, attr_name, Reflector.from_dict(attr_value, data_value))
            else:
                setattr(obj, attr_name, data_value)

        return obj

    @staticmethod
    def from_serial(type_list: TypeList, serials: (list, tuple, set)):
        for one in serials:
            if isinstance(one, type_list.item_type):
                type_list.add(one)
                continue
            item = type_list.item_type()
            Reflector.from_dict(item, one)
            type_list.add(item)

    @staticmethod
    def to_dict(obj: object) -> dict:
        result = {}
        for attr in dir(obj):
            if attr.startswith("__") or callable(getattr(obj, attr)):
                continue
            value = getattr(obj, attr, None)
            if isinstance(value, PRIMITIVE_TYPES):
                result[attr] = value
            else:
                result[attr] = Reflector.to_dict(value)
        return result

    @staticmethod
    def to_yaml(obj: object, file_path: str):
        data = Reflector.to_dict(obj)
        Reflector.dict_to_yaml(data, file_path)

    @staticmethod
    def dict_to_yaml(data: dict, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

    @staticmethod
    def inst(data: dict):
        return Reflector.from_dict(data.__class__(), data)

    @staticmethod
    def clone(obj: object):
        return Reflector.from_dict(obj.__class__(), obj.__dict__)

    @staticmethod
    def invoke(obj: object, method_name: str, *args, **kwargs):
        if not hasattr(obj, method_name):
            return None, False
        method = getattr(obj, method_name)
        if (method is None) or (not callable(method)):
            return None, False
        print("invoke!!!: ", obj, method_name, args, kwargs)
        ret = method(*args, **kwargs)
        return ret, True

    @staticmethod
    def invoke_children(
            obj: object,
            method_name: str,
            invoke_protected: bool = True,
            *args, **kwargs
    ):
        attrs = dir(obj)
        for attr in attrs:
            if not invoke_protected and attr.startswith("_"):
                continue
            if attr.startswith("__"):
                continue
            if callable(getattr(obj, attr)):
                continue
            value = getattr(obj, attr, None)
            if value is None:
                continue
            if isinstance(value, (int, str, float, bool, list, tuple, set, dict)):
                continue
            Reflector.invoke(value, method_name, *args, **kwargs)

        return obj, True

    @staticmethod
    def invoke_self_and_children(
            obj: object,
            method_name: str,
            invoke_protected: bool = True,
            *args, **kwargs
    ):
        ret, success = Reflector.invoke(obj, method_name, *args, **kwargs)
        Reflector.invoke_children(obj, method_name, invoke_protected, *args, **kwargs)
        return ret, success


# ConfigLoader =============================================================================== #

class ConfigUtil:
    @staticmethod
    def load(*config_paths):
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
                    raise ValueError(f"Unsupported configuration file format: {config_path}")
        # Optionally, return a default configuration or raise an exception if no file is found.
        raise FileNotFoundError("No configuration file found in the provided paths.")

    @staticmethod
    def load_and_embed(*config_paths):
        config, config_path = ConfigUtil.load(*config_paths)
        config_dir = os.path.dirname(config_path)
        return ConfigUtil.embed(config, config_dir)

    @staticmethod
    def embed(data: (dict, list, tuple), base_path=''):
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
                    data[key] = ConfigUtil.load(file_path)
                else:
                    ConfigUtil.embed(value, base_path)
            return data

        if isinstance(data, (list, tuple)):
            for i, item in enumerate(data):
                if isinstance(item, str) and item.startswith(cmd):
                    file_name = item[cmd_len:]
                    file_path = os.path.join(base_path, file_name)
                    data[i] = ConfigUtil.load_and_embed(file_path)
                else:
                    ConfigUtil.embed(item, base_path)
            return data

        return data


# Logging =============================================================================== #

class LogUtil:
    @staticmethod
    def load_yaml(*config_path):
        config = ConfigUtil.load(*config_path)
        log_path = getv(config, "", "handlers", "file_handler", "filename")
        if not os.path.exists(log_path):
            log_dir_path = os.path.dirname(log_path)
            os.makedirs(log_dir_path, exist_ok=True)
        # noinspection PyUnresolvedReferences
        logging.config.dictConfig(config)
        return config

    @staticmethod
    def elapsed_async(opts: dict):
        def decorator(func):
            if opts is None:
                return func

            active = opts.get("active", True)
            if not active:
                return func

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = await func(*args, **kwargs)  # Await the function execution
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                logger = logging.getLogger(opts.get("name", "perf"))
                logger.info(f"{func.__name__} completed in {elapsed_time:.2f} seconds")
                return result

            return wrapper

        return decorator


# Text =============================================================================== #

class Text:

    @staticmethod
    def insert_newline_per(text: str, max_len: int = 10) -> str:
        words = text.split()
        new_text = ""
        for i, word in enumerate(words):
            new_text += word + " "
            if (i + 1) % max_len == 0:
                new_text += "\n"
        return new_text


# Time =============================================================================== #

class Time:
    @staticmethod
    def datetime_str() -> str:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


# Collection =============================================================================== #
class Collection:
    @staticmethod
    def insort_ex(container, unit, low=0, high=None, right=True, key=lambda item: item):
        if high is None:
            high = len(container)
        value_unit = key(unit)
        while low < high:
            mid = (low + high) // 2
            unit_mid = container[mid]
            value_mid = key(unit_mid)
            if (value_mid < value_unit) if right else (value_mid > value_unit):
                low = mid + 1
            else:
                high = mid
        container.insert(low, unit)


# FileIO =============================================================================== #
class FileIO:

    @staticmethod
    def fopen(file_path, mode: str = 'rw', encoding: str = 'utf-8', mkdir=True):
        if mkdir:
            parent_directory = os.path.dirname(file_path)
            os.makedirs(parent_directory, exist_ok=True)
        file = open(file_path, mode=mode, encoding=encoding)
        return file
