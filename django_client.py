import os

import requests


class DjangoClient:
    def __init__(self):
        self.url = os.getenv('DJANGO_URL')

        self.responses = []

    def get(self):
        response = requests.get(f'{self.url}entry/')

        self.responses.append(response)

        return response

    def post(self, json):
        response = requests.post(
            f'{self.url}entry/',
            json=json,
        )

        self.responses.append(response)

        return response
