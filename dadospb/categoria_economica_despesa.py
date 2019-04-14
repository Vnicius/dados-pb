from datetime import datetime as dt
from dadospb.utils.createdir import createdir
from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=categoria_economica_despesa'
FILE_NAME = 'categoria_economica_despesa'


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
        return 'Categoria Econômica Despesa'

    def preprocess(self, df):
        return df.rename(columns={
            'CODIGO_CATEGORIA_ECONOMICA_DESPESA': 'cod_categoria_economica_despesa',
            'NOME_CATEGORIA_ECONOMICA_DESPESA': 'nome_categoria_economica_despesa'
        })
