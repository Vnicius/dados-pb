import re
from dadospb.utils.TemplateDownload import TemplateDownload

BASE_URL = 'http://dados.pb.gov.br:80/get{}?nome=acao&exercicio={}'
FILE_NAME = 'acao_governamental'


class DataDownloader(TemplateDownload):
    ''' Classe para realizar o download dos documentos de Dotação Orçamentária '''

    def __init__(self, data_config, args):
        '''
            Construtor da Classe Download

            Attr:
                args (DownloadArgs): argumentos para o download
        '''
        self.data_config = data_config
        super(DataDownloader, self).__init__(base_url=data_config['baseURL'], file_name=data_config['tag'],
                                       only_year=data_config["onlyYear"], periodic_data=data_config["periodicData"],
                                       file_type=args.format, start_year=args.year,
                                       start_month=args.month, end_year=args.untilyear,
                                       end_month=args.untilmonth, merge_data=args.merge,
                                       output_dir=args.output)

    def get_url(self, year, month):
        return self.data_config['baseURL'].format(self.file_type, year, month)

    def get_title(self):
        return self.data_config['title']

    def preprocess(self, df):

        for column in self.data_config['columns']:
            if ('breaked' in column) and (column['breaked']) :
                df[column['name']] = df[column['name']].apply(self.__fix_breaked_data)

        return df.rename(columns={column["name"] : column["rename"] for column in self.data_config["columns"]})
    
    def __fix_breaked_data(self, item):
        
        if item == item:
            return re.sub(r'\s+$', '', item).replace('\n', '')
        
        return item

