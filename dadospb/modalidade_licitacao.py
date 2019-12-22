from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=modalidade_licitacao&exercicio={}'
FILE_NAME = 'modalidade_licitacao'


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
        return 'Modalidade de Licitação'

    def preprocess(self, df):
        return df.rename(columns={
            'EXERCICIO': 'exercicio',
            'CODIGO_MODALIDADE_LICITACAO': 'cod_modalidade_licitacao',
            'NOME_MODALIDADE_LICITACAO': 'nome_modalidade_licitacao'
        })
