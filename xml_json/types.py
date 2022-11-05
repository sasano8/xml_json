class IndexedList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh()

    def get(self, key):
        index = self._index[key]
        return self[index]

    def get_or(self, key, default=None):
        index = self._index[key]
        try:
            return self[index]
        except KeyError:
            return default

    @staticmethod
    def select_key(x):
        return x["id"]

    def refresh(self):
        select_key = self.select_key
        self._index = {select_key(x): i for i, x in enumerate(self)}

    def as_dict(self):
        select_key = self.select_key
        return {select_key(x): x for x in self}