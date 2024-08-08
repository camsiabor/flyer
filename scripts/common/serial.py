class TypeList:
    def __init__(self, item_type, initial=None):
        self.item_type = item_type
        self.items = initial or []
        pass

    def add(self, item):
        if not isinstance(item, self.item_type):
            raise TypeError(f"Item must be of type {self.item_type.__name__}")
        self.items.append(item)
        return self

    def append(self, item):
        return self.add(item)

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

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        yield from self.items
