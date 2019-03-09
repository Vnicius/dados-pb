from datetime import datetime as dt
from utils.createdir import createdir
from utils.TemplateDownload import TemplateDownload
from utils.DownloadArgs import DownloadArgs

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=dotacao&exercicio={}&mes={}'
FILE_NAME = 'dotacao_orcamentaria'
TIME_NOW = dt.now()


class Download(TemplateDownload):
    def __init__(self,
                 file_type='csv',
                 start_year=2000,
                 start_month=1,
                 end_year=0,
                 end_month=0,
                 merge_data=False,
                 output_dir="data"):

        super(Download, self).__init__(base_url=BASE_URL, file_name=FILE_NAME, file_type=file_type,
                                       start_year=start_year, start_month=start_month,
                                       end_year=end_year, end_month=end_month,
                                       only_year=False, merge_data=merge_data,
                                       output_dir=output_dir)

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

    output_dir = ''
    args = DownloadArgs().get_args()

    if args.output:
        output_dir = args.output
    else:
        output_dir = "data_dotacao_orcamentaria"

    Download(start_year=args.year, start_month=args.month,
             end_year=args.untilyear, end_month=args.untilmonth,
             merge_data=args.merge, file_type=args.format,
             output_dir=output_dir).download()
