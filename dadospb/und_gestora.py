from dadospb.utils.TemplateDownload import TemplateDownload
            
BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=unidade_gestora_dadospb&exercicio={}'
FILE_NAME = 'und_gestora'


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
                                       periodic_data=True, only_year=True,
                                       merge_data=args.merge)

    def get_url(self, year, month):
        return BASE_URL.format(self.file_type, year)

    def get_title(self):
        return 'Unidade Gestora'

    def preprocess(self, df):
        return df.rename(columns={
            'EXERCICIO': 'exercicio',
            'CODIGO_UNIDADE_GESTORA': 'cod_und_gestora',
            'SIGLA_UNIDADE_GESTORA': 'sigla_und_gestora',
            'NOME_UNIDADE_GESTORA': 'nome_und_gestora',
            'TIPO_ADMINISTRACAO_UNIDADE_GESTORA': 'tp_adm_und_gestora'
        })
