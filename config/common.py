import random


class PresetCommon:

    @staticmethod
    def dict_get(data: dict, default=None, throw: bool = True, *keys):
        value = data
        for key in keys:
            if isinstance(value, dict):
                if '+' in key:
                    value = PresetCommon.dict_sum(value, key, throw)
                else:
                    value = value.get(key)
            else:
                if throw:
                    value = None
                else:
                    value = default
                break

        if value is None:
            if throw:
                raise KeyError(f"keys not found: {keys}")
            return default

        return value

    @staticmethod
    def dict_sum(data: dict, cmd: str, throw: bool = True) -> any:
        ret = ""
        cmd = cmd.strip()
        if not cmd:
            return ret
        elements = cmd.split('+')
        convert = False
        for element in elements:
            element = element.strip()
            keys = element.split('.')
            value = PresetCommon.dict_get(data, "", throw, *keys)
            if value is None or not value:
                continue
            if isinstance(value, dict):
                if not convert:
                    if ret:
                        ret = {"": ret}
                    else:
                        ret = {}
                    convert = True
                if isinstance(ret, list):
                    ret.append(value)
                if isinstance(ret, dict):
                    ret.update(value)
                continue

            if isinstance(value, (list, tuple)):
                if not convert:
                    if ret:
                        ret = [ret]
                    else:
                        ret = []
                    convert = True

                if isinstance(ret, list):
                    ret.extend(value)
                elif isinstance(ret, dict):
                    ret.update({element: value})
                continue

            if isinstance(value, str):
                value = str(value).strip()
                if not value:
                    continue

                if not convert:
                    if not value.endswith(','):
                        value += ','
                    ret += value
                    continue

                if isinstance(ret, list):
                    ret.append(value)
                elif isinstance(ret, dict):
                    ret.update({element: value})


        return ret

    @staticmethod
    def dict_pick(
            data: dict, cmd: str,
            throw: bool = True, seperator: str = '|'
    ) -> list:
        if data is None:
            if throw:
                raise ValueError("cfg dict is None")
            else:
                return []
        ret = []
        cmd = cmd.strip()
        frags = cmd.split(seperator)
        for frag in frags:
            keys = frag.split('.')
            one = PresetCommon.dict_get(data, None, throw, *keys)
            if one:
                ret.append(one)
        return ret

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
