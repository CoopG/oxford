class Entry:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def pprint(self):
        print(self.name, self.data)
