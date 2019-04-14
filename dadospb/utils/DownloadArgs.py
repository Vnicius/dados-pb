import argparse


class DownloadArgs():
    '''
        Classe com os argumentos padrões para realizar um download

        Attr:
            args (dict): argumentos
    '''

    def __init__(self):
        ''' Construtor da classe DownloadArgs '''

        parser = argparse.ArgumentParser(
            description='Download dos dados do Estado da Paraíba diponíveis em: http://dados.pb.gov.br/')
        parser.add_argument('-m', '--merge',
                            help='unir todos os arquivos', action='store_true')
        parser.add_argument('-f', '--format',
                            help='escolher formato de saída dos arquivos', type=str,
                            choices=['csv', 'json'], default='csv')
        parser.add_argument(
            '--month', help='mês dos documentos', type=int, default=1)
        parser.add_argument(
            '--year', help='ano dos documentos', type=int, default=2000)
        parser.add_argument(
            '--untilmonth', help='mês final dos documentos', type=int, default=0)
        parser.add_argument(
            '--untilyear', help='ano final dos documentos', type=int, default=0)
        parser.add_argument(
            '--db', help='gerar arquivo .db', action='store_true')
        parser.add_argument(
            '-o', '--output', help='diretório de saída', type=str, default='')
        parser.add_argument('-d', '--docs',
                            help='lista de documentos para realizar o download', nargs='*', default=[])
        self.args = parser.parse_args()

    def get_args(self):
        '''
            Retorna os argumentos

            Returns:
                (dict): argumentos
        '''
        return self.args
