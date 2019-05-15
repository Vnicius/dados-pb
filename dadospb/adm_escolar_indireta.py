from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=pagamentos_gestao_pactuada_educacao&exercicio={}&mes={}'
FILE_NAME = 'adm_escolar_indireta'


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
        return 'Administração Escolar Indireta'

    def preprocess(self, df):
        return df.rename(columns={
            'CODIGO_ENVIO': 'cod_envio',
            'COMPETENCIA': 'competencia',
            'CODIGO_ORGANIZACAO_SOCIAL': 'cod_org_social',
            'NOME_ORGANIZACAO_SOCIAL': 'nome_org_social',
            'CODIGO_LANCAMENTO': 'cod_lancamento',
            'DATA_LANCAMENTO': 'dt_lancamento',
            'NUMERO_DOCUMENTO': 'num_doc',
            'TIPO_DOCUMENTO': 'tp_doc',
            'NUMERO_PROCESSO': 'num_processo',
            'CODIGO_CATEGORIA_DESPESA': 'cod_categoria_despesa',
            'NOME_CATEGORIA_DESPESA': 'nome_categoria_depesa',
            'CPFCNPJ_CREDOR': 'cpf_cnpj_credor',
            'NOME_CREDOR': 'nome_credor',
            'VALOR_LANCAMENTO': 'valor_lancamento',
            'OBSERVACAO_LANCAMENTO': 'obs_lancamento',
            'NOME_ESCOLA': 'nome_escola',
            'MUNICIPIO_ESCOLA': 'municipio_escola'
        })
