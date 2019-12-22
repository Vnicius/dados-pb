from dadospb.utils.TemplateDownload import TemplateDownload
            
BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=resumo_folha&exercicio={}&mes={}'
FILE_NAME = 'resumo_folha_pagamento'


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
        return 'Resumo da Folha de Pagamento'

    def preprocess(self, df):
        return df.rename(columns={
            'EXERCICIO': 'exercicio',
            'MES': 'mes',
            'QUADRO': 'quadro',
            'PODER': 'poder',
            'ADMINISTRACAO': 'adm',
            'ORGAO': 'orgao',
            'SECRETARIA': 'secretaria',
            'UNIDADE_TRABALHO': 'und_trabalho',
            'NOME_MUNICIPIO': 'nome_municipio',
            'GRUPO': 'gp',
            'REGIME': 'regime',
            'QUANTIDADE': 'qnt',
            'SOMA_SALARIO_BRUTO': 'soma_salario_bruto'
        })
