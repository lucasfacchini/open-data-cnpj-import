import sys

from parser.parsers import generate_parsers_from_files, EstabeleCsvParser
from parser.generateImportSql import generate_sql_import_from_files
from parser.csv_reader import CsvReader
from parser.importer import SqlImport, MysqlImport
from tools.log import Log
from time import time

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
sql.run_script('schema/mysql/drop-tables-others.sql')
sql.run_script('schema/mysql/create-tables.sql')

t1 = time()
log.info('Analyzing files')
#parsers = generate_parsers_from_files(args['directory'], log)
#if len(parsers) > 0:
#    log.info('Found', len(parsers), 'files')
#else:
#    log.info('No files found.')

#log.info('Truncating tables')
#for parser in parsers:
#    sql.truncate_table(parser.TABLE)

#count = 0
#for parser in parsers:
#    log.info('Importing file', parser.get_name(), '-', count + 1, 'of', len(parsers))
#    sql.run(parser)
#    count += 1


generate_sql_import_from_files(args['directory'], 'schema/mysql/insert-data.sql',0,1)
sql.run_script('schema/mysql/insert-data.sql')
sql.close()

sql = MysqlImport(args['host'], args['port'], args['user'], args['password'], args['database'], log)
generate_sql_import_from_files(args['directory'], 'schema/mysql/insert-data.sql',1,1)
sql.run_script('schema/mysql/insert-data.sql')
sql.close()

sql = MysqlImport(args['host'], args['port'], args['user'], args['password'], args['database'], log)
generate_sql_import_from_files(args['directory'], 'schema/mysql/insert-data.sql',2,1)
sql.run_script('schema/mysql/insert-data.sql')
sql.close()

sql = MysqlImport(args['host'], args['port'], args['user'], args['password'], args['database'], log)
generate_sql_import_from_files(args['directory'], 'schema/mysql/insert-data.sql',3,7)
sql.run_script('schema/mysql/insert-data.sql')

sql.run_script('schema/mysql/rename-tables.sql')
log.info('total time elapsed:',time()-t1)


sql.close()