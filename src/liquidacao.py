from datetime import datetime as dt
from utils.createdir import createdir
from utils.TemplateDownload import TemplateDownload
from utils.DownloadArgs import DownloadArgs

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=liquidacao&exercicio={}&mes={}'
FILE_NAME = 'liquidacao'

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
        return 'Liquidação'

    def preprocess(self, df):
        return df.rename(columns={
          'NU_EXERCICIO': 'num_exercicio',
          'CD_ORGAO': 'cod_orgao',
          'NU_CLASSIFICACAO': 'num_classificacao',
          'CD_UNIDADE': 'cod_und',
          'CD_FUNCAO': 'cod_funcao',
          'CD_SUBFUNCAO': 'cod_subfuncao',
          'CD_PROGRAMA': 'cod_programa',
          'CD_PROJETO_ATIV': 'cod_projeto_ativ',
          'META': 'meta',
          'LOCALIDADE': 'localidade',
          'CD_NATUREZA': 'cod_natureza',
          'CD_FONTE': 'cod_fonte',
          'VALOR': 'valor',
          'NU_EMPENHO': 'num_empenho',
          'DOCUMENTO': 'doc',
          'TIPO_LIQUIDACAO': 'tp_liquidacao',
          'TIPO_DOC_FISCAL': 'tp_doc_fiscal',
          'NUM_NOTAFISCAL': 'num_notafiscal',
          'DATA_NF': 'dt_nf',
          'DATA_MOV': 'dt_mov',
          'DATA_PROC': 'dt_proc',
          'DATA_ATUALIZACAO': 'dt_atualizacao',
          'USUARIO': 'usuario',
          'DOCUMENTO_ORIGEM': 'doc_origem',
          'CD_INSC_RP': 'cod_insc_rp',
          'ANO_INSC_RP': 'ano_insc_rp',
          'ANO_DOC_ORIGEM_LD': 'ano_doc_origem_ld'
        })


if __name__ == '__main__':

    args = DownloadArgs().get_args()

    if not args.output:
        args.output = f'data_{FILE_NAME}'

    Download(args).download()
