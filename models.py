from datetime import datetime


class Entry:
    auto_fields = [
        ('id', 'SERIAL PRIMARY KEY'),
    ]
    save_fields = [
        ('word', 'TEXT'),
        ('data', 'JSONB'),
        ('ts', 'timestamp'),
    ]
    fields = auto_fields + save_fields

    def __init__(self, word, data):
        self.word = word
        self.data = data
        self.ts = datetime.now()

    def pprint(self):
        print(self.word, self.data)
