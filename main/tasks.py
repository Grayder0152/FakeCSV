from config.celery import app
from .services import CSVFile


@app.task
def generate_task(rows, filename, column_separated,
                  string_separated, columns_headers,
                  columns_types, columns_ranges
                  ):

    csv_file = CSVFile(
        rows, filename, column_separated, string_separated,
        columns_headers, columns_types, columns_ranges
    )
    csv_file.generate_csv_file()
