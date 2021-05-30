from mysql.connector.connection import MySQLConnection
from mysql.connector.errors import IntegrityError, DataError
from tqdm import tqdm

class SqlImport():

    def build_insert(self, parser, keys):
        sqlKeys = ','.join(keys)
        sqlValues = ','.join(['%s'] * len(keys))

        return 'INSERT INTO ' + parser.TABLE + '(' + sqlKeys + ') VALUES (' + sqlValues + ')'


class MysqlImport(SqlImport):
    BATCH_SIZE = 5000

    def __init__(self, host, port, user, password, db, log):
        self.context = MySQLConnection(host=host, port=port, user=user, password=password, database=db)
        self.cursor = self.context.cursor()
        self.log = log

    def run(self, parser, limit=0):
        lines = []
        keys = []
        pbar = tqdm(total=parser.get_size())
        count = 0

        while limit == 0 or count <= limit:
            lines = parser.parse_bulk(self.BATCH_SIZE)
            count += len(lines)
            if len(lines) == 0:
                break

            try:
                lines_in_tuples = list(map(lambda line: tuple(line.values()), lines))
                keys = lines[0].keys()
                self.cursor.executemany(self.build_insert(parser, keys), lines_in_tuples)
                pbar.update(len(lines))
            except (IntegrityError, DataError) as e:
                self.log.error(str(e))

            lines = []

        self.context.commit()

    def run_script(self, filepath):
        for line in open(filepath):
            self.cursor.execute(line)
        self.log.info('Ran script', filepath)

    def truncate_table(self, table):
        self.cursor.execute('TRUNCATE TABLE ' + table)

    def close(self):
        self.context.commit()
        self.cursor.close()
        self.context.close()