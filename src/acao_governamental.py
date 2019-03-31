from datetime import datetime as dt
from utils.createdir import createdir
from utils.TemplateDownload import TemplateDownload
from utils.DownloadArgs import DownloadArgs

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=acao&exercicio={}'
FILE_NAME = 'acao_governamental'

class Download(TemplateDownload):
    ''' Classe para realizar o download dos documentos de Dotação Orçamentária '''

    def __init__(self, args):
        '''
            Construtor da Classe Download

            Attr:
                args (DownloadArgs): argumentos para o download
        '''

        super(Download, self).__init__(base_url=BASE_URL, file_name=FILE_NAME, 
                                       file_type=args.format, start_year=args.year,
                                       end_year=args.untilyear, output_dir=args.output, 
                                       periodic_data=True, only_year=True)

    def get_url(self, year, month):
        return BASE_URL.format(self.file_type, year)
    
    def get_title(self):
        return 'Ação Governamental'

    def preprocess(self, df):
        return df.rename(columns={
            'EXERCICIO': 'exercicio',
            'CODIGO_ACAO': 'cd_acao',
            'NOME_ACAO': 'nome_acao'
        })


if __name__ == '__main__':

    args = DownloadArgs().get_args()

    if not args.output:
        args.output = f'data_{FILE_NAME}'

    Download(args).download()
