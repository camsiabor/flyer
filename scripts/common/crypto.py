import base64
import json

from cryptography.fernet import Fernet

DICT_HINT_DEF = 'p_box_p'


class CryptoUtil:

    @staticmethod
    def gen_key(password):
        # Use a password to generate a key. This is a simple way to ensure a consistent key from a string.
        return base64.urlsafe_b64encode(password.ljust(32)[:32].encode('utf-8'))


    @staticmethod
    def encrypt(
            info: any,
            key: any,
    ) -> [str]:
        if isinstance(key, str):
            key = CryptoUtil.gen_key(key)
        fernet = Fernet(key)
        if isinstance(info, str):
            info_bytes = info.encode('utf-8')
        else:
            info_bytes = info
        # Encrypt the bytes
        encrypted_info = fernet.encrypt(info_bytes)
        encrypted_info = base64.b64encode(encrypted_info).decode('utf-8')
        return encrypted_info

    @staticmethod
    def encrypt_probe(
            info: dict,
            dict_hint: str = DICT_HINT_DEF
    ) -> bool:
        content = info.get(dict_hint, None)
        return content is not None

    @staticmethod
    def decrypt(
            encrypted_data: any,
            key: any,
    ) -> [str]:
        if isinstance(key, str):
            key = CryptoUtil.gen_key(key)
        fernet = Fernet(key)
        encrypted_data = base64.b64decode(encrypted_data)
        decrypted_bytes = fernet.decrypt(encrypted_data)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str

    @staticmethod
    def encrypt_dict(
            info_dict: dict,
            key: any,
            dict_hint: str = DICT_HINT_DEF
    ) -> [dict]:
        if dict_hint and len(dict_hint) > 0:
            content = info_dict.get(dict_hint, None)
            if content is not None:
                return info_dict
        info_bytes = json.dumps(info_dict).encode('utf-8')
        encrypted_info = CryptoUtil.encrypt(info_bytes, key)
        return {dict_hint: encrypted_info}

    @staticmethod
    def decrypt_dict(
            encrypted_dict: dict,
            key: any,
            dict_hint: str = DICT_HINT_DEF,
    ) -> dict:
        encrypted_data = encrypted_dict.get(dict_hint, None)
        if encrypted_data is None:
            return encrypted_dict
        decrypted_str = CryptoUtil.decrypt(encrypted_data, key)
        decrypted_dict = json.loads(decrypted_str)
        return decrypted_dict
