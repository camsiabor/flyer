
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
        for placeholder, target in params.items():
            if isinstance(target, (list, tuple)):
                length = len(target)
                if length > 0:
                    target = target[cycle % length]
                else:
                    target = ""
            token = f"{prefix}{placeholder}{suffix}"
            result = result.replace(token, target)
        return result
