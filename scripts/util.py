import glob
import os


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def file_count(target, suffix="*.png"):
    pattern = os.path.join(target, suffix)
    files = glob.glob(pattern)
    return len(files)


def str_exist(s):
    s = s.strip()
    return s is not None and len(s) > 0


def color_string_to_tuple(c_str):
    r = 0
    g = 0
    b = 0
    a = 0
    if c_str is None or len(c_str) == 0:
        return a, g, b, a

    c_str = c_str.lower()

    if c_str[0] == '#':
        if len(c_str) >= 7:
            r = int(c_str[1:3], 16)  # Extract and convert the red component
            g = int(c_str[3:5], 16)  # Extract and convert the green component
            b = int(c_str[5:7], 16)  # Extract and convert the blue component

        if len(c_str) >= 9:
            a = int(c_str[7:9], 16)  # Extract and convert the alpha component
        else:
            a = 255
        return r, g, b, a

    if c_str[0] == 'r':
        c_str = (c_str
                 .replace('rgba', '').replace('rgb', '')
                 .replace('(', '').replace(')', ''))

    color_values = c_str.strip().split(",")
    color_values = [int(value) for value in color_values]

    if len(color_values) < 3:
        raise ValueError(f"Invalid color string: {c_str}")

    if len(color_values) >= 3:
        r, b, g = color_values[0], color_values[1], color_values[2]
        a = 255

    if len(color_values) >= 4:
        a = color_values[3]

    return r, g, b, a


class FileIO:
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

    @staticmethod
    def walk_des(
            src_dir, des_dir,
            callback_dir, callback_file,
            file_ext=None,
            depth_limit=-1
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
                callback_dir(root, des_path, dirs, files)
            if callback_file is not None:
                for file in files:
                    src_file = os.path.join(root, file)
                    des_file = os.path.join(des_path, file)
                    callback_file(src_file, des_file)
        pass
