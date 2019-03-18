from datetime import datetime as dt
from utils.createdir import createdir
from utils.TemplateDownload import TemplateDownload
from utils.DownloadArgs import DownloadArgs

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=tipo_modalidade_pagamento'
FILE_NAME = 'tp_modalidade_pagamento'

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
        return 'Tipo Modalidade de Pagamento'

    def preprocess(self, df):
        return df.rename(columns={
            'codigo_modalidade': 'cod_modalidade',
            'descricao_modalidade': 'desc_modalidade'
        })


if __name__ == '__main__':

    args = DownloadArgs().get_args()

    if not args.output:
        args.output = "data_tp_modalidade_pagamento"

    Download(args).download()
