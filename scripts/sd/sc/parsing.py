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
            remain = 'Steps:' + fragments[1].strip()

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
    def meta_to_markdown(meta: dict, list_display: list, wrap_max=96) -> str:
        d = SDParser.meta_to_dict(meta)
        display_all = (list_display is not None) and ('All' in list_display)
        pos = ""
        neg = ""
        pos_neg = ""
        if display_all or ('Positive Prompt' in list_display):
            pos = d.get('Positive Prompt', '')
            pos = TextUtil.wrap_lines_ex(pos, wrap_max)
            pos_neg = f"```\n{pos}\n```\n"

        if display_all or ('Negative Prompt' in list_display):
            neg = d.get('Negative Prompt', '')
            neg = TextUtil.wrap_lines_ex(neg, wrap_max)
            pos_neg += f"```\n{neg}\n```\n"

        if display_all:
            list_display = None

        table = MarkdownUtil.dict_to_table(
            meta=d, headers="",
            excludes=['Positive Prompt', 'Negative Prompt'],
            includes=list_display,
        )
        return pos_neg + table
