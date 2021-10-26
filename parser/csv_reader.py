import csv
import sys

DELIMITER = ';'
ENCODING = 'ISO-8859-1'

class CsvReader:
    def __init__(self, filename, log=None):
        self.filename = filename
        self.log = log
        self._file = None

    def open(self):
        self._file = open(self.filename, 'r', encoding=ENCODING)

        return self._file

    def read(self):
        for line in self._file:
            reader = csv.reader([line.replace('\0','')], delimiter=DELIMITER)
            for row in reader:
                return row

    def count_lines(self, chunk_size=65536):
        count = 0
        with self.open() as csvfile:
            while True:
                chunk = csvfile.read(chunk_size)
                if not chunk:
                    break
                count += chunk.count('\n')

        return count

    def close(self):
        self._file.close()