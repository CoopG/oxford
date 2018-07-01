import argparse
from datetime import datetime
import json
import os

from pprintpp import pprint as pp
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--entry')
parser.add_argument('--lexicalCategory')
args = parser.parse_args()


class Oxford:
    def __init__(self, lang):
        self.base_url = os.getenv('URL')
        self.headers = {
            'app_id': os.getenv('ID'),
            'app_key': os.getenv('KEY'),
        }
        self.lang = lang


    def get(self, path, **params):
        return requests.get(
            f'{self.base_url}/{path}',
            params=params,
            headers=self.headers
        )

    def search(self, q):
        return self.get(f'search/{self.lang}/translations=en', q=q)

    def entry(self, q):
        r = self.get(f'entries/{self.lang}/{q}/translations=en')

        with open(os.path.join('entries', q + '.json'), 'w') as f:
            f.write(r.text)

        return r


ox = Oxford('de')
if args.entry:
    r = ox.entry(args.entry)
    pp(r.json())
