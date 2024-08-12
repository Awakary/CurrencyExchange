import json

from error import Error


class View:

    def __init__(self, data):
        self.data = data

    def to_json(self):
        if isinstance(self.data, Error):
            self.data = self.data.__dict__
        return json.dumps(self.data)

    def from_json(self):
        pass