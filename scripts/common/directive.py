class Directive:

    def __init__(
            self,
            line: str = "",
            category: str = "",
            prefix="<OvO>",
            suffix="</OvO>",
    ):
        self.line = line
        self.category = category
        self.parse(line)
        pass

    def parse(self):
        return self

    pass


class Directorate:
    pass
