from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=tipos_de_orcamento'
FILE_NAME = 'tipos_orcamento'


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
        return 'Tipos de Orçamentos'

    def preprocess(self, df):
        return df.rename(columns={
            'CD_TIPO_ORCAMENTO': 'cod_tipo_orcamento',
            'DS_TIPO_ORCAMENTO': 'desc_tipo_orcamento'
        })
