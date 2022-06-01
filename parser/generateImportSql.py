rom parser.utils import *
import glob
import abc
from parser.csv_reader import CsvReader

class Parser:
    def __init__(self, reader):
        print('log')
        #self.reader = reader
        #self.size = self.reader.count_lines()
        #self.reader.open()

    def read_line(self):
        return self.reader.read()

    def get_size(self):
        return self.size

    def get_name(self):
        return self.reader.filename

    @abc.abstractmethod
    def parse_line(self):
        pass

    def parse_bulk(self, size):
        count = 0
        lines = []
        while count < size:
            line = self.parse_line()
            if line is None:
                break
            lines.append(line)
            count += 1

        return lines

    def close(self):
        self.reader.close()


class CnpjCsvParser(Parser):
    TABLE = 'empresa2'
    FILE_PATTERN = '*EMPRECSV'
    FIELDS = 'id,razao_social,codigo_natureza_juridica,qualificacao_responsavel,@capital_social,@porte'
    EXTRA = " set capital_social = cast(replace(replace(@capital_social,'.',''),',','.') as float), porte = cast(@porte as signed)"

class SocioCsvParser(Parser):
    TABLE = 'socio2'
    FILE_PATTERN = '*SOCIOCSV'
    FIELDS = 'id_empresa,tipo_pessoa,nome,cpf_cnpj,codigo_qualificacao,data,@dummy,cpf_representante_legal,nome_representante_legal,codigo_qualificacao_representante_legal'
    EXTRA = ''


class EstabeleCsvParser(Parser):
    TABLE = 'estabelecimento2'
    FILE_PATTERN = '*ESTABELE'
    FIELDS = 'id_empresa, subsidiaria, codigo_verificador,matriz_filial, fantasia, situacao_cadastral, data_situacao_cadastral, motivo_situacao_cadastral,@dummy,@dummy1, data_abertura,@cnae, @cnae2, endereco_tipo_logradouro, endereco_logradouro, endereco_numero,endereco_complemento,endereco_bairro,endereco_cep,endereco_uf,endereco_codigo_municipio,@telefone1_ddd,telefone1_numero,@telefone2_ddd,telefone2_numero, @fax_ddd,fax_numero,email'
    EXTRA = " set cnae_principal=substring_index(@cnae,',',1),cnae_secundaria=substring_index(@cnae2,',',1),telefone1_ddd = substring(@telefone1_ddd,-2),telefone2_ddd=substring(@telefone2_ddd,-2),fax_ddd=substring(@fax_ddd,-2),cnpj=concat(id_empresa,subsidiaria,codigo_verificador)"


class OptanteSimplesCsvParser(Parser):
    TABLE = 'optante_simples2'
    FILE_PATTERN = '*SIMPLES.CSV*'
    FIELDS = 'id_empresa,simples,simples_inicio,simples_fim,simei,simei_inicio,simei_fim'
    EXTRA = ""


class CnaeCsvParser(Parser):
    TABLE = 'cnae2'
    FILE_PATTERN = '*CNAECSV'
    FIELDS = 'cnae,descricao'
    EXTRA = ''

class MunicipioCsvParser(Parser):
    TABLE = 'municipio2'
    FILE_PATTERN = '*MUNICCSV'
    FIELDS = 'codigo,nome'
    EXTRA = ''

class NaturezaJuridicaCsvParser(Parser):
    TABLE = 'natureza_juridica2'
    FILE_PATTERN = '*NATJUCSV'
    FIELDS = 'codigo,descricao'
    EXTRA = ''

class QualSocioCsvParser(Parser):
    TABLE = 'qualificacao_socio2'
    FILE_PATTERN = '*QUALSCSV'
    FIELDS = 'codigo,descricao'
    EXTRA = ''

class PaisCsvParser(Parser):
    TABLE = 'pais2'
    FILE_PATTERN = '*PAISCSV'
    FIELDS = 'codigo,descricao'
    EXTRA = ''

class MotivoSituacaoCadastralCsvParser(Parser):
    TABLE = 'motivo_situacao_cadastral2'
    FIELDS = 'codigo,descricao'
    EXTRA = ''


def formatSql(filename, tablename, fields, extra):
    return "load data local infile '{}' into table {} character set 'latin1' fields terminated by ';' enclosed by '\"' lines terminated by '\\n' ({}) {};".format(filename, tablename, fields, extra)

def generate_sql_import_from_files(directory, sqlFile):
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
    with open(sqlFile, 'w') as f:
        parserMotivo = MotivoSituacaoCadastralCsvParser(CsvReader('data/motivo_situacao_cadastral.csv'))
        f.write(formatSql('data/motivo_situacao_cadastral.csv',parserMotivo.TABLE,parserMotivo.FIELDS,parserMotivo.EXTRA)+"\n")
        for parser in parsers:
            files_from_pattern = glob.glob(directory + '/' + parser.FILE_PATTERN)
            for filepath in files_from_pattern:
                f.write(formatSql(filepath, parser.TABLE, parser.FIELDS, parser.EXTRA) + "\n")
