import os

import requests


class DjangoClient:
    def __init__(self):
        self.url = os.getenv('DJANGO_URL')
        user = os.getenv('DJANGO_USER')
        password = os.getenv('DJANGO_PASS')
        self.auth = (user, password)

        self.responses = []

    def get(self):
        response = requests.get(f'{self.url}entry/', auth=self.auth)

        self.responses.append(response)

        return response

    def post(self, json):
        response = requests.post(f'{self.url}entry/', json=json, auth=self.auth)

        self.responses.append(response)

        return response
