from datetime import datetime as dt
from dadospb.utils.createdir import createdir
from dadospb.utils.TemplateDownload import TemplateDownload
from dadospb.utils.DownloadArgs import DownloadArgs

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=dotacao&exercicio={}&mes={}'
FILE_NAME = 'dotacao_orcamentaria'

class Download(TemplateDownload):
    ''' Classe para realizar o download dos documentos de Dotação Orçamentária '''

    def __init__(self, args):
        '''
            Construtor da Classe Download

            Attr:
                args (DownloadArgs): argumentos para o download

        '''

        super(Download, self).__init__(base_url=BASE_URL, file_name=FILE_NAME, file_type=args.format,
                                       start_year=args.year, start_month=args.month,
                                       end_year=args.untilyear, end_month=args.untilmonth,
                                       only_year=False, merge_data=args.merge,
                                       output_dir=args.output)

    def get_url(self, year, month):
        return BASE_URL.format(self.file_type, year, month)
    
    def get_title(self):
        return 'Dotação Orçamentária'

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

    args = DownloadArgs().get_args()

    if not args.output:
        args.output = f'data_{FILE_NAME}'

    Download(args).download()
