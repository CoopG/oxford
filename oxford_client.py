from datetime import datetime
import os

from pprintpp import pprint as pp
import requests

from psql import PostgresClient

class OxfordClient:
    def __init__(self, lang='de'):
        self.base_url = os.getenv('URL')
        self.headers = {
            'app_id': os.getenv('ID'),
            'app_key': os.getenv('KEY'),
        }
        self.lang = lang

    def get(self, path, **params):
        response = requests.get(
            f'{self.base_url}/{path}',
            params=params,
            headers=self.headers
        )

        return response

    def search(self, q=None, output=True):
        response = self.get(f'search/{self.lang}/translations=en', q=q)

        data = response.json()

        if output:
            print(data)

        return data

    def entry(self, q=None, output=True):
        if q is None:
            q = input()
        response = self.get(f'entries/{self.lang}/{q}/translations=en')

        with open(os.path.join('cache', 'entries', q + '.json'), 'w') as f:
            f.write(response.text)

        data = response.json()

        if output:
            print(data)

        return data
