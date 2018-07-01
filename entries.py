from datetime import datetime as dt
from glob import iglob
import json
from os.path import getmtime
import re


class Entries:
    GLOB = 'cache/entries/*.json'
    RE = re.compile(r'entries\/(?P<name>.*)\.json')

    def __init__(self):
        self.get_entries()

    def get_entries(self):
        entries = {}

        for path in iglob(self.GLOB):
            try:
                data = self.load(path)
            except json.JSONDecodeError:
                continue

            data['mtime'] = dt.fromtimestamp(getmtime(path))
            entry = self.RE.search(path).group('name')

            entries[entry] = data

        self.entries = entries

    def load(self, path):
        with open(path) as f:
            data = json.load(f)
        return data


e = Entries()
