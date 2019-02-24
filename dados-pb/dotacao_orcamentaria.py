from datetime import datetime as dt
from utils.createdir import createdir
from utils.dowloadtemplate import DownloadTemplate

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=dotacao&exercicio={}&mes={}'
FILE_NAME = 'dotacao_orcamentaria'
TIME_NOW = dt.now()


class Download(DownloadTemplate):
    def __init__(self,
                 file_type='csv',
                 start_year=2000,
                 start_month=1,
                 end_year=TIME_NOW.year,
                 end_month=TIME_NOW.month,
                 merge_data=False):

        super(Download, self).__init__(base_url=BASE_URL, file_name=FILE_NAME, file_type=file_type,
                                       start_year=start_year, start_month=start_month,
                                       end_year=end_year, end_month=end_month,
                                       only_year=False, merge_data=merge_data)

    def get_url(self, year, month):
        return BASE_URL.format(self.file_type, year, month)

    def preprocess(self, df):
        return df.rename(columns={
            'unidade_gestora': 'und_gestora',
            'exercicio': 'exercicio',
            'unidade_orcamentaria': 'und_orcamentaria',
            'funcao': 'funcao',
            'subfuncao': 'subfuncao',
            'programa': 'programa',
            'acao': 'acao',
            'meta': 'meta',
            'localidade': 'localidade',
            'categoria': 'categoria',
            'grupo_despesa': 'gp_depesa',
            'modalidade': 'modalidade',
            'elemento_despesa': 'element_depesa',
            'fonte_recurso': 'fonte_recurso',
            'valor_orcado': 'valor_orcado'
        })


if __name__ == '__main__':
    Download(start_year=2018, start_month=12,
             merge_data=True, file_type='json').download()
