class TextUtil:

    @staticmethod
    def replace(
            template: str,
            replacements: dict,
            prefix: str = "$$",
            suffix: str = "$$"
    ):
        """
        Replaces placeholders in a template string with values from a dictionary.

        :param suffix:
        :param prefix:
        :param template: The template string containing placeholders.
        :param replacements: A dictionary where each key is a placeholder in the template
                             and its value is the replacement string.
        :return: A new string with all placeholders replaced by their corresponding values.
        """
        if replacements is None or len(replacements) == 0:
            return template
        result = template
        for placeholder, replacement in replacements.items():
            token = f"{prefix}{placeholder}{suffix}"
            result = result.replace(token, replacement)
        return result
