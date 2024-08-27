import json


class View:

    """Класс перевода в json"""

    def __init__(self, data):
        self.data = data

    def to_json(self) -> json:
        if isinstance(self.data, list) and not all(isinstance(i, dict) for i in self.data):
            self.data = [obj.__dict__ for obj in self.data]
        elif not isinstance(self.data, dict) and not isinstance(self.data, list):
            self.data = self.data.__dict__
        return json.dumps(self.data)
