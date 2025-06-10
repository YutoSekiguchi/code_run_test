class Column(list):
    def sum(self):
        return sum(self)

class DataFrame:
    def __init__(self, data):
        self._data = {k: list(v) for k, v in data.items()}
    def __getitem__(self, key):
        return Column(self._data[key])
    def sum(self):
        return {k: sum(v) for k, v in self._data.items()}
    def __repr__(self):
        return f"DataFrame({self._data})"

__version__ = '0.0.0-stub'
