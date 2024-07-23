import random


class PresetCommon:

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
