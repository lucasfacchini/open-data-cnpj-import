import sys

from parser.parsers import generate_parsers_from_files, EstabeleCsvParser
from parser.csv_reader import CsvReader
from parser.importer import SqlImport, MysqlImport
from tools.log import Log

DEFAULT_DIRECTORY = 'data/output-extract'

def parse_args():
    if len(sys.argv) < 5:
        print('usage: mysql_import.py <host> <port> <user> <password> <database> <directory>')

        exit()

    return {
        'host': sys.argv[1],
        'port': sys.argv[2],
        'user': sys.argv[3],
        'password': sys.argv[4],
        'database': sys.argv[5],
        'directory': sys.argv[6]
    }

args = parse_args()
directory = args['directory'] if args['directory'] else DEFAULT_DIRECTORY
log = Log()
sql = MysqlImport(args['host'], args['port'], args['user'], args['password'], args['database'], log)
log.info('Creating schema')
sql.run_script('schema/mysql/drop-tables.sql')
sql.run_script('schema/mysql/create-tables.sql')

log.info('Analyzing files')
parsers = generate_parsers_from_files(directory, log)

if len(parsers) > 0:
    log.info('Found', len(parsers), 'files')
else:
    log.info('No files found.')

log.info('Truncating tables')
for parser in parsers:
    sql.truncate_table(parser.TABLE)

count = 0
for parser in parsers:
    log.info('Importing file', parser.get_name(), '-', count + 1, 'of', len(parsers))
    sql.run(parser)
    count += 1

sql.close()