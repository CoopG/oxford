from collections import defaultdict
import os

import requests
from django_client import DjangoClient
from renderers import Entry, Search


class OxfordClient:
    def __init__(self, lang='de'):
        self.base_url = os.getenv('URL')
        self.headers = {
            'app_id': os.getenv('ID'),
            'app_key': os.getenv('KEY'),
        }
        self.django = DjangoClient()
        self.lang = lang
        self.cache = defaultdict(list)

    def get(self, path, **params):
        response = requests.get(
            f'{self.base_url}{path}',
            params=params,
            headers=self.headers,
        )

        self.cache['response'].append(response)

        return response

    def search(self, q=None, output=True):
        response = self.get(f'search/{self.lang}/translations=en', q=q)

        if response.status_code == 200:
            data = response.json()

            search = Search(data)

            if output:
                print(search)

            self.cache['search'].append(search)

    def entry(self, q=None, output=True):
        if q is None:
            q = input()

        response = self.get(f'entries/{self.lang}/{q}/translations=en')

        if response.status_code == 404:
            self.search(q)

        elif response.status_code == 200:
            data = response.json()

            entry = Entry(data)

            if output:
                print(entry)

            self.cache['entry'].append(entry)

            django_response = self.django.post({
                'name': q,
                'data': data,
            })

            self.cache['django_response'].append(django_response)
