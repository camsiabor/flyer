import logging
import random
import re

from typing import Union


class TextUtil:

    @staticmethod
    def replace(
            src: str,
            params: dict,
            cycle: int = 0,
            prefix: str = "$$",
            suffix: str = "$$"
    ):
        """
        Replaces placeholders in a template string with values from a dictionary.

        :param cycle:
        :param suffix:
        :param prefix:
        :param src: The template string containing placeholders.
        :param params: A dictionary where each key is a placeholder in the template
                             and its value is the replacement string.
        :return: A new string with all placeholders replaced by their corresponding values.
        """
        if params is None or len(params) == 0:
            return src
        result = src
        cycle_current = cycle
        for placeholder, target in params.items():
            if placeholder.startswith("_"):
                placeholder = placeholder[1:]
                target = ""
            else:
                if isinstance(target, (list, tuple)):
                    if cycle < 0:
                        cycle_current = random.randint(0, 142857)
                    length = len(target)
                    if length > 0:
                        target = target[cycle_current % length]
                    else:
                        target = ""
            target = str(target)
            token = f"{prefix}{placeholder}{suffix}"
            result = result.replace(token, target)
        return result

    @staticmethod
    # Example command processor function
    def replace_cmd_processer(cmd: str, params: dict, *args):
        if cmd == 'rand' or cmd == 'randint':
            is_integer = cmd == 'randint'
            range_text = args[0]
            if not range_text:
                raise ValueError("range_text is empty")
            if '~' not in range_text:
                range_text = '0~' + range_text
            random_value = TextUtil.to_num(range_text, is_integer)
            return f"{random_value:.3f}"

        if cmd == 'n' or cmd == 'num' or cmd == 'int' or cmd == 'float':
            target = None
            for arg in args:
                try:
                    if not arg or arg.startswith('$'):
                        continue
                    target = TextUtil.to_num(arg)
                    break
                except Exception as ex:
                    logging.warning(f"Error converting arg {arg} to number: {ex}")
            if target is None:
                return None
            if cmd == 'int':
                return f"{int(target)}"
            return f"{target:.3f}"

        # Add more command handling as needed
        else:
            raise ValueError("unrecognized command: " + cmd)

    @staticmethod
    def replace_cmd(
            s: str,
            params: dict = None,
            # Define the regex pattern to find ${command|arg1|arg2|...|argN} format
            pattern=r'\$\{(\w+)\|([^\}]+)\}',
            command_processor=None
    ) -> str:
        # Function to replace each match
        def replacer(match):
            command = match.group(1)
            args = match.group(2).split('|')
            for i, arg in enumerate(args):
                if arg.startswith('$$'):
                    args[i] = TextUtil.replace(arg, params)

            # Use the command_processor to generate the replacement string
            if command_processor is not None:
                ret = command_processor(command, params, *args)
            else:
                ret = TextUtil.replace_cmd_processer(command, params, *args)
            if ret is None:
                return match.group(0)
            return ret

        # Replace all matches in the string using the replacer function
        replaced_string = re.sub(pattern, replacer, s)
        return replaced_string

    @staticmethod
    def wrap_lines(text: str, line_length=72, sep_word=",") -> str:
        words = text.split(sep_word)
        current_line = ""
        lines = []

        for word in words:
            word = word.strip()
            if current_line:
                # Check if adding the word plus a comma and space exceeds the line length
                if len(current_line) + len(word) + 2 > line_length:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line += ", " + word
            else:
                current_line = word

        if current_line:
            lines.append(current_line)

        ret = ",\n".join(lines)
        ret = ret.replace(', ,', ',')
        ret = ret.replace(',,', ',')
        ret = ret.replace('\n\n', '\n')
        ret = ret.replace('\n\n', '\n')
        return ret

    @staticmethod
    def wrap_lines_ex(text: str, line_length=72, sep_word=",", sep_line="\n") -> str:
        lines = text.split(sep_line)
        for i, line in enumerate(lines):
            lines[i] = TextUtil.wrap_lines(line, line_length, sep_word)
        return sep_line.join(lines)

    @staticmethod
    def to_num(
            text: str,
            is_int: bool = False
    ) -> Union[int, float]:

        if isinstance(text, (int, float)):
            return text

        ret = text.strip()

        if not ret:
            raise ValueError("text is empty")

        if '~' in text:
            min_str, max_str = ret.split('~')
            if is_int:
                ret = random.randint(int(min_str), int(max_str))
            else:
                ret = random.uniform(float(min_str), float(max_str))

        if is_int:
            return int(ret)
        return float(ret)


# MarkdownUtil =============================================================================================


class MarkdownUtil:
    @staticmethod
    def dict_to_table(meta: dict, headers="", includes=None, excludes=None) -> str:
        if not headers:
            headers = "| Key | Value |\n"
        sperator = "| --- | --- |\n"
        rows = []
        for k, v in meta.items():
            if excludes is not None and k in excludes:
                continue
            if includes is not None and k not in includes:
                continue
            rows.append(f"| {k} | {v} |")
        table = headers + sperator + "\n".join(rows)
        return table
