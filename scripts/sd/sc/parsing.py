from scripts.common.textutil import TextUtil, MarkdownUtil


class SDParser:

    @staticmethod
    def meta_to_dict(meta: dict, seperator: str = ',') -> dict:
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

            parts = remain.split(seperator)
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
    def meta_to_markdown(meta: dict, wrap_max=72) -> str:
        d = SDParser.meta_to_dict(meta)
        pos = d.get('Positive Prompt', '')
        neg = d.get('Negative Prompt', '')
        pos = TextUtil.wrap_lines_ex(pos, wrap_max)
        neg = TextUtil.wrap_lines_ex(neg, wrap_max)
        pos_neg = f"```\n{pos}\n```\n```\n{neg}\n```\n"
        table = MarkdownUtil.dict_to_table(
            d, "",
            'Positive Prompt', 'Negative Prompt'
        )
        return pos_neg + table
