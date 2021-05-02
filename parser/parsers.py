from parser.utils import *
import glob
from parser.csv_reader import CsvReader

class Parser:
    def __init__(self, reader):
        self.reader = reader
        self.size = self.reader.count_lines()
        self.generator = self.reader.read()

    def read_line(self):
        try:
            return next(self.generator)
        except StopIteration:
            return None

    def get_size(self):
        return self.size

    def get_name(self):
        return self.reader.filename


class CnpjCsvParser(Parser):
    TABLE = 'empresa'
    FILE_PATTERN = '*EMPRECSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'id': row[0],
            'razao_social': row[1],
            'codigo_natureza_juridica': row[2],
            'qualificacao_responsavel': row[3],
            'capital_social': parse_float(row[4]),
            'porte': parse_int(row[5])
        } if row else None

class SocioCsvParser(Parser):
    TABLE = 'socio'
    FILE_PATTERN = '*SOCIOCSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'id_empresa': row[0],
            'tipo_pessoa': parse_int(row[1]),
            'nome': row[2],
            'cpf_cnpj': row[3],
            'codigo_qualificacao': row[4],
            'data': parse_date(row[5]),
            'cpf_representante_legal': row[7],
            'nome_representante_legal': row[8],
            'codigo_qualificacao_representante_legal': row[9],
        } if row else None

class EstabeleCsvParser(Parser):
    TABLE = 'estabelecimento'
    FILE_PATTERN = '*ESTABELE'

    def parse_line(self):
        row = self.read_line()
        return {
            'id_empresa': row[0],
            'subsidiaria': row[1],
            'codigo_verificador': row[2],
            'cnpj': row[0] + row[1] + row[2],
            'matriz_filial': parse_int(row[3]),
            'fantasia': row[4],
            'situacao_cadastral': row[5],
            'data_situacao_cadastral': parse_date(row[6]),
            'motivo_situacao_cadastral': row[7],
            'data_abertura': parse_date(row[10]),
            'cnae_principal': parse_cnae(row[11]),
            'cnae_secundaria': parse_cnae(row[12]),
            'endereco_tipo_logradouro': row[13],
            'endereco_logradouro': row[14],
            'endereco_numero': row[15],
            'endereco_complemento': row[16],
            'endereco_bairro': row[17],
            'endereco_cep': row[18],
            'endereco_uf': row[19],
            'endereco_codigo_municipio': row[20],
            'telefone1_ddd': row[21][-2:],
            'telefone1_numero': row[22],
            'telefone2_ddd': row[23][-2:],
            'telefone2_numero': row[24],
            'fax_ddd': row[25][-2:],
            'fax_numero': row[26],
            'email': row[27]
        } if row else None

class OptanteSimplesCsvParser(Parser):
    TABLE = 'optante_simples'
    FILE_PATTERN = '*SIMPLES.CSV*'

    def parse_line(self):
        row = self.read_line()
        return {
            'id_empresa': row[0],
            'simples': row[1],
            'simples_inicio': parse_date(row[2]),
            'simples_fim': parse_date(row[3]),
            'simei': row[4],
            'simei_inicio': parse_date(row[5]),
            'simei_fim': parse_date(row[6])
        } if row else None

class CnaeCsvParser(Parser):
    TABLE = 'cnae'
    FILE_PATTERN = '*CNAECSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'cnae': row[0],
            'descricao': row[1]
        } if row else None

class MunicipioCsvParser(Parser):
    TABLE = 'municipio'
    FILE_PATTERN = '*MUNICCSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'codigo': row[0],
            'nome': row[1]
        } if row else None

class NaturezaJuridicaCsvParser(Parser):
    TABLE = 'natureza_juridica'
    FILE_PATTERN = '*NATJUCSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'codigo': row[0],
            'descricao': row[1]
        } if row else None

class QualSocioCsvParser(Parser):
    TABLE = 'qualificacao_socio'
    FILE_PATTERN = '*QUALSCSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'codigo': row[0],
            'descricao': row[1]
        } if row else None

class PaisCsvParser(Parser):
    TABLE = 'pais'
    FILE_PATTERN = '*PAISCSV'

    def parse_line(self):
        row = self.read_line()
        return {
            'codigo': row[0],
            'descricao': row[1]
        } if row else None

class MotivoSituacaoCadastralCsvParser(Parser):
    TABLE = 'motivo_situacao_cadastral'

    def parse_line(self):
        row = self.read_line()
        return {
            'codigo': row[0],
            'descricao': row[1]
        } if row else None

def generate_parsers_from_files(directory, log):
    parsers = [
        CnpjCsvParser,
        SocioCsvParser,
        EstabeleCsvParser,
        OptanteSimplesCsvParser,
        CnaeCsvParser,
        MunicipioCsvParser,
        NaturezaJuridicaCsvParser,
        QualSocioCsvParser,
        PaisCsvParser
    ]
    parser_instances = [MotivoSituacaoCadastralCsvParser(CsvReader('data/motivo_situacao_cadastral.csv', log))]

    for parser in parsers:
        files_from_pattern = glob.glob(directory + '/' + parser.FILE_PATTERN)
        parser_instances += map(lambda filepath: parser(CsvReader(filepath)), files_from_pattern)

    return parser_instances
