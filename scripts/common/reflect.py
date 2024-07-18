import os

import yaml

from scripts.common.serial import TypeList

VALUE_TYPES = (int, str, float, bool)
SERIAL_TYPES = (list, tuple, set)
PRIMITIVE_TYPES = (int, str, float, bool, list, tuple, set, dict)


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
    def clone_dict(d: dict, accept_types=None):
        ret = {}
        for key, value in d.items():
            if isinstance(value, VALUE_TYPES):
                ret[key] = value
                continue
            if isinstance(value, SERIAL_TYPES):
                ret[key] = Reflector.clone_serial(value, accept_types)
                continue
            if accept_types is not None and isinstance(value, accept_types):
                value = Reflector.to_dict(value)
            if isinstance(value, dict):
                ret[key] = Reflector.clone_dict(value, accept_types)
        return ret

    @staticmethod
    def clone_serial(serial: (list, tuple, set), accept_types=None):
        ret = []
        for item in serial:
            if isinstance(item, VALUE_TYPES):
                ret.append(item)
                continue
            if isinstance(item, SERIAL_TYPES):
                ret.append(Reflector.clone_serial(item, accept_types))
                continue
            if accept_types is not None and isinstance(item, accept_types):
                item = Reflector.to_dict(item)
            if isinstance(item, dict):
                ret.append(Reflector.clone_dict(item, accept_types))
        return ret

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
