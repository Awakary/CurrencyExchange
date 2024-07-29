import json


class View:

    def __init__(self, data):
        self.data = data

    def to_json(self, columns):
        if 'rate' in columns[-1]:
            rates = [list(i) for i in self.data if all([(isinstance(j, int | float)) for j in i])]
            currencies = [list(i) for i in self.data if list(i) not in rates]
            fields = ['id', 'name', 'code', 'sign']
            for i in range(len(rates)):
                rates[i][1] = dict(zip(fields, [c for c in currencies if c[0] == rates[i][1]][0]))
                rates[i][2] = dict(zip(fields, [c for c in currencies if c[0] == rates[i][2]][0]))
            self.data = rates
        content = []
        for row in self.data:
            content.append(dict(zip([column[0] for column in columns], row)))
        if len(content) == 1:
            content = content[0]
        return json.dumps(content)

    def from_json(self):
        pass