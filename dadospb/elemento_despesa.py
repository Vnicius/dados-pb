from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=elemento_despesa'
FILE_NAME = 'elemento_depesa'


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
        return 'Elemento da Despesa'

    def preprocess(self, df):

        df['NOME_ELEMENTO_DESPESA'] = df['NOME_ELEMENTO_DESPESA'].apply(
            lambda x: x.replace('\n', ''))

        return df.rename(columns={
            'CODIGO_ELEMENTO_DESPESA': 'cod_elemento_despesa',
            'NOME_ELEMENTO_DESPESA': 'nome_elemento_despesa'
        })
