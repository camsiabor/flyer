# FileIO =============================================================================== #
import json
import os

import yaml


class FileUtil:

    @staticmethod
    def fopen(file_path, mode: str = 'rw', encoding: str = 'utf-8', mkdir=True):
        if mkdir:
            parent_directory = os.path.dirname(file_path)
            os.makedirs(parent_directory, exist_ok=True)
        file = open(file_path, mode=mode, encoding=encoding)
        return file

    @staticmethod
    def load(file_path, mode: str = 'r', encoding: str = 'utf-8'):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"None found: {file_path}")
        with open(file_path, mode=mode, encoding=encoding) as config_file:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(config_file), file_path
            if file_path.endswith('.json'):
                return json.load(config_file), file_path
            if file_path.endswith('.py'):
                return eval(config_file.read()), file_path
            raise ValueError(f"Unsupported config file format: {file_path}")
        pass

    @staticmethod
    def walk(src_dir, callback_file, file_ext=None, depth_limit=-1):
        # Depth limit of -1 means no limit
        src_dir = os.path.normpath(src_dir)
        base_depth = src_dir.rstrip(os.path.sep).count(os.path.sep)
        for root, dirs, files in os.walk(src_dir):
            depth = root.count(os.path.sep) - base_depth
            if -1 < depth_limit < depth:
                dirs[:] = []  # Clear dirs list to prevent further walking
                continue
            if file_ext:
                files = [f for f in files if f.endswith(file_ext)]
            for file in files:
                src_file = os.path.join(root, file)
                callback_file(src_file)

    # noinspection PyTypeChecker
    @staticmethod
    def walk_des(
            src_dir, des_dir,
            callback_dir, callback_file,
            file_ext=None,
            depth_limit=-1,
            callback_args=None,
    ):
        # Depth limit of -1 means no limit
        src_dir = os.path.normpath(src_dir)
        des_dir = os.path.normpath(des_dir)
        base_depth = src_dir.rstrip(os.path.sep).count(os.path.sep)
        for root, dirs, files in os.walk(src_dir):
            depth = root.count(os.path.sep) - base_depth
            if -1 < depth_limit < depth:
                dirs[:] = []  # Clear dirs list to prevent further walking
                continue
            # Create the corresponding destination directory if it doesn't exist
            relative_path = os.path.relpath(root, src_dir)
            des_path = os.path.join(des_dir, relative_path)
            os.makedirs(des_path, exist_ok=True)
            if file_ext:
                files = [f for f in files if f.endswith(file_ext)]
            if callback_dir is not None:
                callback_dir(root, des_path, dirs, files, callback_args)
            if callback_file is not None:
                for file in files:
                    src_file = os.path.join(root, file)
                    des_file = os.path.join(des_path, file)
                    callback_file(src_file, des_file, callback_args)
        pass
