import random
from collections.abc import Iterable

from typing import List, Union


# Collection =============================================================================== #

class Collection:

    @staticmethod
    def nextv(data: any, step: int = 1, throw_if_none: bool = False):
        ret = data
        if data is not None:
            if isinstance(data, (list, tuple)):
                if len(data) <= 0:
                    return None
                ret = data[step - 1]
            elif isinstance(data, dict):
                for i in range(step):
                    ret = next(iter(data))
        if ret is None and throw_if_none:
            raise ValueError("data is None")
        return ret

    @staticmethod
    def randv(data: any, throw_if_none: bool = False):

        ret = data

        if isinstance(data, dict):
            size = len(data)
            if size <= 0:
                ret = None
            elif size == 1:
                ret = next(iter(data.values()))
            else:
                data = list(data.values())

        if isinstance(data, (list, tuple, Iterable)):
            size = len(data)
            if size <= 0:
                ret = None
            elif size == 1:
                ret = data[0]
            else:
                ret = random.choice(data)

        if ret is None and throw_if_none:
            raise ValueError("data is None")

        return ret

    @staticmethod
    def is_blank(data: any) -> bool:

        if data is None:
            return True

        if isinstance(data, str):
            data = data.strip()
            return not data

        if isinstance(data, (list, tuple)):
            if len(data) <= 0:
                return True
            for v in data:
                if not Collection.is_blank(v):
                    return False
            return True

        if isinstance(data, dict):
            if len(data) <= 0:
                return True
            for k, v in data.items():
                if not Collection.is_blank(v):
                    return False
            return True

        return False

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

            if isinstance(value, (list, tuple)):
                if not key.isdigit():
                    if throw:
                        raise TypeError(f"list index must be integer: {key} |\n {value}")
                    return default
                key = int(key)
                if key < 0:
                    key = len(value) + key
                if key < 0 or key >= len(value):
                    if throw:
                        raise IndexError(f"list index out of range: {key} |\n {value}")
                    return default
                value = value[key]
                continue

            if isinstance(value, dict):
                # has '+'
                if '+' in key:
                    value = Collection.dict_sum(value, key, throw)
                    continue

                # has ':'
                if ':' in key:
                    key, subkey = key.split(':')
                    value = value.get(key)

                    if isinstance(value, (list, tuple)):
                        value = value[int(subkey)]
                        continue

                    if isinstance(value, dict):
                        value = value.get(subkey)
                        continue

                    if hasattr(value, subkey):
                        value = getattr(value, subkey)
                        continue

                    if throw:
                        raise KeyError(f"keys not found: {subkey} | {value}")

                    continue

                # default
                value = value.get(key)
                continue

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
    def list_cross(a: list, b: list) -> list:
        ret = []
        for i in a:
            for j in b:
                is_i_str = isinstance(i, str)
                is_j_str = isinstance(j, str)
                is_i_list = isinstance(i, (list, tuple))
                is_j_list = isinstance(j, (list, tuple))

                if is_i_str and i and not i.startswith(','):
                    i += ','

                if is_i_str and is_j_str:
                    ret.append(f"{i} {j}")
                    continue

                if is_i_str and is_j_list:
                    for jj in j:
                        ret.append(f"{i} {jj}")
                    continue

                if is_i_list and is_j_str:
                    for ii in i:
                        if ii and not ii.startswith(','):
                            ii += ','
                        ret.append(f"{ii} {j}")
                    continue

                if is_i_list and is_j_list:
                    ij = Collection.list_cross(i, j)
                    ret.append(ij)
                    continue

        return ret

    @staticmethod
    def list_crosses(*lists) -> list:
        size = len(lists)
        if size <= 0:
            return []
        ret = lists[0]
        for i in range(1, size):
            ret = Collection.list_cross(ret, lists[i])
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

    @staticmethod
    def clamp(data: any, prefix: str = "", suffix: str = "", skip_empty: bool = True):

        if data is None:
            return None

        if isinstance(data, str):
            if skip_empty and not data:
                return ""
            return prefix + data + suffix

        if isinstance(data, (list, tuple)):
            size = len(data)
            clone = []
            for i in range(size):
                v = Collection.clamp(data[i], prefix, suffix, skip_empty)
                clone.append(v)
            return clone

        if isinstance(data, dict):
            clone = {}
            for k, v in data.items():
                clone[k] = Collection.clamp(v, prefix, suffix, skip_empty)
            return clone

        return Collection.clamp(str(data), prefix, suffix, skip_empty)

    @staticmethod
    def join(data: any, sep: str) -> str:
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        if isinstance(data, (list, tuple)):
            ret = sep.join(data).replace(",,", ",")
            return ret
        return str(data)

    @staticmethod
    def roll_pick_parse(data: any, picks: any) -> dict:

        if isinstance(picks, dict):
            return picks

        if picks is None or picks == "" or picks == "+":
            picks = "+".join(data.keys())
        elif picks == '*':
            picks = "*".join(data.keys())
        elif picks == '0':
            picks = Collection.nextv(data, True)

        if not isinstance(picks, str):
            raise ValueError(f"picks type error: {picks}")

        pick_dict = {}
        list_and = picks.strip().split("*")
        for one_and in list_and:
            list_plus = one_and.strip().split("+")
            if len(list_plus) <= 0:
                continue
            pick_path = []
            for element in list_plus:
                element = element.strip()
                if not element:
                    continue
                pathes = element.split(".")
                pick_path.append(pathes)
            pick_dict[one_and] = pick_path

        return pick_dict

    @staticmethod
    def roll_container_append(container: list, convert: any):
        if convert is None:
            return container
        if isinstance(convert, (list, tuple)):
            return container
        if isinstance(convert, str):
            convert = convert.strip()
            if convert:
                container.append(convert)
            return container
        raise ValueError(f"convert type error: {convert}")

    @staticmethod
    def roll(
            data: any,
            container: list,
            picks: Union[None, str, List[str]] = None,
            depth: int = 0
    ) -> any:
        if data is None:
            return None
        if isinstance(data, str):
            return data

        if depth > 0:
            if isinstance(data, dict):
                return Collection.roll_dict(data, container, picks)
            if isinstance(data, (list, tuple)):
                return Collection.roll_list(data, container, picks)
            return str(data)

        pick_dict = Collection.roll_pick_parse(data, picks)
        for k, pick_path in pick_dict.items():
            container_sub = []
            convert = Collection.roll(data, container_sub, pick_path, depth + 1)
            Collection.roll_container_append(container_sub, convert)
            if len(container_sub) <= 0:
                continue
            serial = (", ".join(container_sub).strip().replace(',,', ','))
            container.append(serial)

        return container

    @staticmethod
    def roll_dict(
            data: dict,
            container: list,
            picks: Union[None, str, List[str]] = None,
            depth: int = 0,
    ) -> list:
        if data is None:
            return container
        if container is None:
            container = []

        if picks is None or len(picks) <= 0:
            for k, v in data.items():
                convert = Collection.roll(v, container, picks, depth + 1)
                Collection.roll_container_append(container, convert)
            return container

        if isinstance(picks, str):
            sub = data[picks]
            convert = Collection.roll(sub, container, None, depth + 1)
            Collection.roll_container_append(container, convert)
            return container

        for pick in picks:
            if isinstance(pick, str):
                Collection.roll(data, container, pick, depth + 1)
                continue
            if isinstance(pick, (list, tuple)):
                key = pick[0]
                sub = data[key]
                convert = Collection.roll(sub, container, pick[1:], depth + 1)
                Collection.roll_container_append(container, convert)
                continue
            raise ValueError(f"picks type error: {pick}")

        return container

    @staticmethod
    def roll_list(
            data: list,
            container: list,
            picks: Union[None, str, List[str]] = None,
            depth: int = 0,
    ) -> any:
        if data is None:
            return None
        size = len(data)
        if size <= 0:
            return None
        if size == 1:
            ret = data[0]
        else:
            rand = random.randint(0, size - 1)
            ret = data[rand]
        ret = Collection.roll(ret, container, picks, depth + 1)
        return ret
