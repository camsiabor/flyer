import datetime


# get / set / clone =============================================================================== #


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



# NumUtil =============================================================================== #

class NumUtil:
    @staticmethod
    def is_odd(num: int) -> bool:
        return num % 2 == 1

    @staticmethod
    def is_even(num: int) -> bool:
        return num % 2 == 0

    @staticmethod
    def odd_to_even(num: int, direction: int = 1) -> int:
        return (num + direction) if NumUtil.is_odd(num) else num

    @staticmethod
    def round_to_even(num: any, direction: int = 1):
        return NumUtil.odd_to_even(round(num), direction)
