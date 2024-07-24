import random


class PresetCommon:

    @staticmethod
    def get(cfg: dict, default=KeyError, *keys):
        value = cfg
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                value = default
        if value is None:
            value = default
        if isinstance(value, KeyError):
            raise KeyError(f"KeyError: {keys}")
        return value

    @staticmethod
    def to_array(data):
        ret = []
        repeat = 1
        for v in data:
            if isinstance(v, int):
                if v < 0:
                    v = random.randint(1, abs(v))
                repeat = v
                continue
            if isinstance(v, str):
                if repeat <= 0:
                    continue
                for i in range(repeat):
                    ret.append(v)
                repeat = 1
        return ret
