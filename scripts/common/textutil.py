import random
import re
import sys


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

            token = f"{prefix}{placeholder}{suffix}"
            result = result.replace(token, target)
        return result

    @staticmethod
    # Example command processor function
    def replace_cmd_processer(cmd, *args):
        if cmd == 'rand':
            range_min = 0
            range_max = sys.maxsize
            if not args or len(args) > 0:
                range_str = args[0]
                range_min, range_max = map(float, range_str.split('~'))
            random_value = random.uniform(range_min, range_max)
            return f"{random_value:.3f}"
        # Add more command handling as needed
        else:
            raise ValueError("unrecognized command: " + cmd)

    @staticmethod
    def replace_cmd(
            s: str,
            # Define the regex pattern to find ${command|arg1|arg2|...|argN} format
            pattern=r'\$\{(\w+)\|([^\}]+)\}',
            command_processor=None
    ) -> str:
        # Function to replace each match
        def replacer(match):
            command = match.group(1)
            args = match.group(2).split('|')
            # Use the command_processor to generate the replacement string
            if command_processor is not None:
                return command_processor(command, *args)
            return TextUtil.replace_cmd_processer(command, *args)

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

        return ",\n".join(lines)

    @staticmethod
    def wrap_lines_ex(text: str, line_length=72, sep_word=",", sep_line="\n") -> str:
        lines = text.split(sep_line)
        for i, line in enumerate(lines):
            lines[i] = TextUtil.wrap_lines(line, line_length, sep_word)
        return sep_line.join(lines)


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
