import psycopg2

from models import Entry


class PostgresClient:
    def __init__(self, dbname='oxford', user='dan'):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    @property
    def table(self):
        return ','.join(' '.join(field) for field in Entry.fields)

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def save(self, entry):
        columns = ','.join(field[0] for field in Entry.save_fields)
        fstrs = ','.join('%s' for _ in Entry.save_fields)
        values = tuple(getattr(entry, field[0]) for field in Entry.save_fields)

        self.execute(
            f'INSERT INTO entries ({columns}) VALUES ({fstrs});',
            values,
        )

    def flush(self):
        self.execute('DROP TABLE IF EXISTS entries;')
        self.execute(f'CREATE TABLE ENTRIES({self.table});')


postgres_client = PostgresClient()
