class SDParser:

    @staticmethod
    def meta_to_dict(meta: dict) -> dict:
        ret = {}

        for k, v in meta.items():
            if not isinstance(v, str):
                continue
            v_str = str(v).strip()
            if k != 'parameters':
                ret[k] = v_str
                continue
            fragments = v_str.split('Negative prompt:')
            ret['Positive Prompt'] = fragments[0].strip()
            remain = fragments[1].strip()
            fragments = remain.split('Steps:')
            ret['Negative Prompt'] = fragments[0].strip()
            remain = fragments[1].strip()

            parts = remain.split(',')
            # Iterate over each part
            for part in parts:
                # Check if the part contains a colon, indicating a key-value pair
                if ':' in part:
                    # Split by the first colon to separate key and value
                    key, value = part.split(':', 1)
                    # Trim whitespace
                    key = key.strip()
                    value = value.strip()
                    # Store the value in the dictionary
                    ret[key] = value

        return ret

    @staticmethod
    def meta_to_markdown(meta: dict) -> str:
        ret = []
        d = SDParser.meta_to_dict(meta)
        for k, v in d.items():
            ret.append(f"{k}:\n```{v}```")
        return "\n".join(ret)
