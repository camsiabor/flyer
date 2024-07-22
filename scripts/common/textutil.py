import random


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
