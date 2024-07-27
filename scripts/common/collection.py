import math
import random


# CPack =============================================================================== #
class CPack:

    def __init__(
            self,
            content: any,
            prefix: any = None,
            suffix: any = None,
            weight_min=1,
            weight_max=1,
    ):
        self.content = content
        self.prefix = prefix
        self.suffix = suffix
        self.weight_min = weight_min
        self.weight_max = weight_max
        pass

    def unpack(self):
        if self.weight_max <= 0:
            return None

        weight = 1
        if self.weight_min == self.weight_max:
            weight = self.weight_min
        else:
            if isinstance(self.weight_min, int) and isinstance(self.weight_max, int):
                weight = random.randint(self.weight_min, self.weight_max)
            else:
                weight = math.floor(random.uniform(self.weight_min, self.weight_max))

        if weight <= 0:
            return None

        if self.prefix is not None:
            self.content = self.prefix + self.content

        return self.content

    pass


# Collection =============================================================================== #

class Collection:

    @staticmethod
    def dict_merge(ret: dict, *dicts):
        if dicts is None:
            return ret
        for d in dicts:
            if d is None:
                continue
            if not isinstance(d, dict):
                continue
            for k, v in d.items():
                ret[k] = v
        return ret

    @staticmethod
    def dict_get(data: dict, default=None, throw: bool = True, *keys):
        value = data
        for key in keys:
            if isinstance(value, dict):
                if '+' in key:
                    value = Collection.dict_sum(value, key, throw)
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
            value = Collection.dict_get(data, "", throw, *keys)
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
            data: dict,
            cmd: str,
            throw: bool = True,
            seperator: str = '|',
            merge: bool = True,
    ) -> list:
        if data is None:
            if throw:
                raise ValueError("cfg dict is None")
            else:
                return []
        array = []
        cmd = cmd.strip()
        frags = cmd.split(seperator)
        for frag in frags:
            keys = frag.split('.')
            one = Collection.dict_get(data, None, throw, *keys)
            if one:
                array.append(one)
        if not merge:
            return array
        ret = []
        for one in array:
            if isinstance(one, (list, tuple)):
                ret.extend(one)
            else:
                ret.append(one)
        return ret

    @staticmethod
    def list_unpack(data):
        ret = []
        repeat = 1
        for v in data:
            if v is None:
                continue
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

    @staticmethod
    def list_insort(container, unit, low=0, high=None, right=True, key=lambda item: item):
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

    # generate a function that merge dict

    @staticmethod
    def list_merge(ret: list, *lists):
        if lists is None:
            return ret
        for li in lists:
            if li is None:
                continue
            if not isinstance(li, (list, tuple)):
                continue
            for v in li:
                ret.append(v)
        return ret