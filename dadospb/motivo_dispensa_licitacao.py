from dadospb.utils.TemplateDownload import TemplateDownload
            
BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=dispensa_licitacao&exercicio={}'
FILE_NAME = 'motivo_dispensa_licitacao'


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
        return 'Motivo da Dispensa de Licitação'

    def preprocess(self, df):
        return df.rename(columns={
            'EXERCICIO': 'exercicio',
            'CODIGO_MOTIVO_DISPENSA_LICITACAO': 'cod_motivo_dispensa_licitacao',
            'DESCRICAO_MOTIVO_DISPENSA_LICITACAO': 'desc_motivo_dispensa_licitacao'
        })
