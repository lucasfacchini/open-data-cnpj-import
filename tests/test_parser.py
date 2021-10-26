import unittest
from parser.parsers import *
from parser.csv_reader import CsvReader

class TestParser(unittest.TestCase):

    def test_parse_cnpj(self):
        cnpj_parser = CnpjCsvParser(CsvReader('tests/test-files/EMPRECSV'))

        self.assertEqual({
            'id': '11111111',
            'razao_social': 'LOREM IPSUM',
            'codigo_natureza_juridica': '2135',
            'qualificacao_responsavel': '50',
            'capital_social': 1000.00,
            'porte': 5
        }, cnpj_parser.parse_line())

        self.assertEqual({
            'id': '11111111',
            'razao_social': 'LOREM IPSUM',
            'codigo_natureza_juridica': '2135',
            'qualificacao_responsavel': '50',
            'capital_social': None,
            'porte': None
        }, cnpj_parser.parse_line())
        cnpj_parser.close()

    def test_parse_cnpj_bulk(self):
        cnpj_parser = CnpjCsvParser(CsvReader('tests/test-files/EMPRECSV'))
        self.assertEqual(1, len(cnpj_parser.parse_bulk(2)))
        cnpj_parser.close()

        cnpj_parser = CnpjCsvParser(CsvReader('tests/test-files/EMPRECSVBULK'))
        self.assertEqual(2, len(cnpj_parser.parse_bulk(2)))
        self.assertEqual(0, len(cnpj_parser.parse_bulk(2)))
        cnpj_parser.close()

    def test_parse_socio(self):
        socio_parser = SocioCsvParser(CsvReader('tests/test-files/SOCIOCSV'))

        self.assertEqual({
            'id_empresa': '00000000',
            'tipo_pessoa': 2,
            'nome': 'JOHN DOE',
            'cpf_cnpj': '***111111**',
            'codigo_qualificacao': '30',
            'data': '2010-11-05',
            'cpf_representante_legal': '***111111**',
            'nome_representante_legal': 'JOHN DOE 2',
            'codigo_qualificacao_representante_legal': '15',
        }, socio_parser.parse_line())
        socio_parser.close()

    def test_parse_estabele(self):
        estabele_parser = EstabeleCsvParser(CsvReader('tests/test-files/ESTABELE'))

        self.assertEqual({
            'id_empresa': '00000000',
            'subsidiaria': '0001',
            'codigo_verificador': '41',
            'cnpj': '00000000000141',
            'matriz_filial': 1,
            'fantasia': 'FANTASIA',
            'situacao_cadastral': '2',
            'data_situacao_cadastral': '2005-11-03',
            'motivo_situacao_cadastral': '1',
            'data_abertura': '1994-05-30',
            'cnae_principal': '4712100',
            'cnae_secundaria': '4712101',
            'endereco_tipo_logradouro': 'RUA',
            'endereco_logradouro': 'ROBERTO DE CAMPOS BICUDO',
            'endereco_numero': '44',
            'endereco_complemento': 'FRENTE',
            'endereco_bairro': 'CATIAPOA',
            'endereco_cep': '11370470',
            'endereco_uf': 'SP',
            'endereco_codigo_municipio': '7121',
            'telefone1_ddd': '13',
            'telefone1_numero': '11111111',
            'telefone2_ddd': '13',
            'telefone2_numero': '11111111',
            'fax_ddd': '13',
            'fax_numero': '11111111',
            'email': 'test@hotmail.com'
        }, estabele_parser.parse_line())
        estabele_parser.close()

    def test_parse_optante_simples(self):
        optante_simples_parser = OptanteSimplesCsvParser(CsvReader('tests/test-files/SIMPLES.CSV'))

        self.assertEqual({
            'id_empresa': '00000000',
            'simples': 'N',
            'simples_inicio': '2007-07-01',
            'simples_fim': '2018-02-01',
            'simei': 'N',
            'simei_inicio': '2010-01-01',
            'simei_fim': '2018-02-01'
        }, optante_simples_parser.parse_line())

        self.assertEqual({
            'id_empresa': '00000000',
            'simples': 'N',
            'simples_inicio': None,
            'simples_fim': None,
            'simei': 'N',
            'simei_inicio': None,
            'simei_fim': None
        }, optante_simples_parser.parse_line())
        optante_simples_parser.close()

    def test_parse_cnae(self):
        cnae_parser = CnaeCsvParser(CsvReader('tests/test-files/CNAECSV'))

        self.assertEqual({
            'cnae': '0111301',
            'descricao': 'Cultivo de arroz'
        }, cnae_parser.parse_line())
        cnae_parser.close()


    def test_parse_minicipio(self):
        municipio_parser = MunicipioCsvParser(CsvReader('tests/test-files/MUNICCSV'))

        self.assertEqual({
            'codigo': '0001',
            'nome': 'GUAJARA-MIRIM'
        }, municipio_parser.parse_line())
        municipio_parser.close()

    def test_parse_natureza_juridica(self):
        natureza_juridica_parser = NaturezaJuridicaCsvParser(CsvReader('tests/test-files/NATJUCSV'))

        self.assertEqual({
            'codigo': '0000',
            'descricao': 'NATUREZA JURIDICA NAO INFORMADA'
        }, natureza_juridica_parser.parse_line())
        natureza_juridica_parser.close()


    def test_parse_qual_socio(self):
        qual_socio_parser = QualSocioCsvParser(CsvReader('tests/test-files/QUALSCSV'))

        self.assertEqual({
            'codigo': '00',
            'descricao': 'NAO INFORMADA'
        }, qual_socio_parser.parse_line())
        qual_socio_parser.close()


    def test_parse_pais(self):
        pais_parser = PaisCsvParser(CsvReader('tests/test-files/PAISCSV'))

        self.assertEqual({
            'codigo': '000',
            'descricao': 'COLIS POSTAUX'
        }, pais_parser.parse_line())
        pais_parser.close()