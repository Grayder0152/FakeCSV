import csv

from faker import Faker
from django.conf import settings


class CSVFile:
    PATH = f'{settings.MEDIA_ROOT}/csv-files'

    def __init__(self, rows: int, filename: str, column_separated: str,
                 string_separated: str, columns_headers: list,
                 columns_types: list, columns_ranges: dict):
        self.rows = rows
        self.filename = filename
        self.column_separated = column_separated
        self.string_separated = string_separated
        self.columns_headers = columns_headers
        self.columns_types = columns_types
        self.columns_ranges = columns_ranges

    @staticmethod
    def _generate_fake_data():
        fake = Faker()
        fake_data = {
            'FN': fake.name,
            'E': fake.email,
            'DN': fake.domain_name,
            'CN': fake.company,
            'I': fake.random.randint,
            'D': fake.date
        }
        return fake_data

    def generate_csv_file(self):
        with open(f'{self.PATH}/{self.filename}.csv', 'w') as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=self.column_separated,
                lineterminator=self.string_separated
            )

            writer.writerow(self.columns_headers)

            fake_data = self._generate_fake_data()
            for _ in range(self.rows):
                row = []
                for i in range(len(self.columns_types)):
                    column_type = self.columns_types[i]
                    if column_type == 'I':
                        data = fake_data[column_type](*self.columns_ranges[self.columns_headers[i]])
                    else:
                        data = fake_data[column_type]()
                    row.append(data)
                writer.writerow(row)
