# Collection =============================================================================== #
class Collection:
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
