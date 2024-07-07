class TypeList:
    def __init__(self, item_type, initial=None):
        self.item_type = item_type
        self.items = initial or []

    def add(self, item):
        if not isinstance(item, self.item_type):
            raise TypeError(f"Item must be of type {self.item_type.__name__}")
        self.items.append(item)

    def get(self, index):
        return self.items[index]

    def remove(self, index):
        del self.items[index]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        yield from self.items
