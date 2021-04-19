import csv
import sys

DELIMITER = ';'
ENCODING = 'ISO-8859-1'

class CsvReader:
    def __init__(self, filename, log=None):
        self.filename = filename
        self.log = log

    def read(self):
        file = open(self.filename, 'r', encoding=ENCODING)
        with file as csvfile:
            for line in csvfile:
                reader = csv.reader([line.replace('\0','')], delimiter=DELIMITER)
                for row in reader:
                    yield row

    def count_lines(self, chunk_size=65536):
        count = 0
        with open(self.filename, 'r', encoding=ENCODING) as csvfile:
            while True:
                chunk = csvfile.read(chunk_size)
                if not chunk:
                    break
                count += chunk.count('\n')

        return count