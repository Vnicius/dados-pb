from datetime import datetime as dt
from dadospb.utils.createdir import createdir
from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=grupo_natureza_despesa'
FILE_NAME = 'gp_natureza_despesa'


class Download(TemplateDownload):
    ''' Classe para realizar o download dos documentos de Dotação Orçamentária '''

    def __init__(self, args):
        '''
            Construtor da Classe Download

            Attr:
                args (DownloadArgs): argumentos para o download
        '''

        super(Download, self).__init__(base_url=BASE_URL, file_name=FILE_NAME, file_type=args.format,
                                       output_dir=args.output, periodic_data=False)

    def get_url(self, year, month):
        return BASE_URL.format(self.file_type)

    def get_title(self):
        return 'Grupo Natureza de Despesa'

    def preprocess(self, df):
        return df.rename(columns={
            'CODIGO_GRUPO_NATUREZA_DESPESA': 'cod_gp_natureza_despesa',
            'NOME_GRUPO_NATUREZA_DESPESA': 'nome_gp_natureza_despesa'
        })
