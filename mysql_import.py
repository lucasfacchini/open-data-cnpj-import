import sys

from parser.parsers import generate_parsers_from_files
from parser.importer import MysqlImport
from tools.log import Log

DEFAULT_DIRECTORY = 'data/output-extract'

def parse_args():
    if len(sys.argv) < 5:
        print('usage: mysql_import.py <host> <port> <user> <password> <database> <directory>')

        exit()

    args = {
        'host': sys.argv[1],
        'port': sys.argv[2],
        'user': sys.argv[3],
        'password': sys.argv[4],
        'database': sys.argv[5]
    }

    if len(sys.argv) > 6:
        args['directory'] = sys.argv[6]
    else:
        args['directory'] = DEFAULT_DIRECTORY

    return args


args = parse_args()
log = Log()
sql = MysqlImport(args['host'], args['port'], args['user'], args['password'], args['database'], log)
log.info('Creating schema')
sql.run_script('schema/mysql/drop-tables.sql')
sql.run_script('schema/mysql/create-tables.sql')

log.info('Analyzing files')
parsers = generate_parsers_from_files(args['directory'], log)

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
