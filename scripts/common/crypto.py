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
    def encrypt_dict(
            info_dict: dict,
            key: any,
            base64_encode: bool = True,
            dict_hint: str = DICT_HINT_DEF
    ) -> [dict]:

        if dict_hint and len(dict_hint) > 0:
            content = info_dict.get(dict_hint, None)
            if content is not None:
                return info_dict

        if isinstance(key, str):
            key = CryptoUtil.gen_key(key)

        fernet = Fernet(key)
        # Convert the dictionary to a JSON string and then to bytes
        info_bytes = json.dumps(info_dict).encode('utf-8')
        # Encrypt the bytes
        encrypted_info = fernet.encrypt(info_bytes)
        if base64_encode:
            encrypted_info = base64.b64encode(encrypted_info).decode('utf-8')
        if dict_hint and len(dict_hint) > 0:
            ret = {dict_hint: encrypted_info}
            return ret
        return encrypted_info

    @staticmethod
    def decrypt_dict(
            encrypted_data,
            key: any,
            base64_encoded: bool = True,
            dict_hint: str = DICT_HINT_DEF,
    ) -> [dict]:

        if isinstance(key, str):
            key = CryptoUtil.gen_key(key)

        fernet = Fernet(key)
        if isinstance(encrypted_data, dict):
            encrypted_data = encrypted_data.get(dict_hint, None)
        if base64_encoded:
            encrypted_data = base64.b64decode(encrypted_data)
        decrypted_bytes = fernet.decrypt(encrypted_data)
        decrypted_str = decrypted_bytes.decode('utf-8')
        decrypted_dict = json.loads(decrypted_str)
        return decrypted_dict
