import os

import requests

from models import Entry


class OxfordClient:
    def __init__(self, lang='de'):
        self.base_url = os.getenv('URL')
        self.headers = {
            'app_id': os.getenv('ID'),
            'app_key': os.getenv('KEY'),
        }
        self.django_url = os.getenv('DJANGO_URL')
        self.lang = lang
        self.responses = []

    def get(self, path, **params):
        response = requests.get(
            f'{self.base_url}{path}',
            params=params,
            headers=self.headers,
        )

        self.responses.append(response)

        return response

    def post(self, json):
        response = requests.post(
            f'{self.django_url}entry/',
            json=json,
        )

        return response

    def search(self, q=None, output=True):
        response = self.get(f'search/{self.lang}/translations=en', q=q)

        if response.status_code == 200:
            data = response.json()

            if output:
                print(data)

            return data

    def entry(self, q=None, output=True):
        if q is None:
            q = input()

        response = self.get(f'entries/{self.lang}/{q}/translations=en')

        if response.status_code == 200:
            data = response.json()

            entry = Entry(q, data)

            if output:
                entry.pprint()

            self.post({
                'name': q,
                'data': data,
            })

            return data
