from argparse import ArgumentParser

import psycopg2

parser = ArgumentParser()
parser.add_argument('--flush', action='store_true')
args = parser.parse_args()


class PostgresClient:
    def __init__(self, dbname='oxford', user='dan'):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def execute(self, query):
        return self.cursor.execute(query)


postgres_client = PostgresClient()

if args.flush:
    postgres_client.execute("""
    DROP TABLE IF EXISTS entries;
    CREATE TABLE entries (
        id int,
        data JSONB,
        timestamp timestamp
    );
    """)
