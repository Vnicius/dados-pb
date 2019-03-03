import argparse

class DownloadArgs():
    def __init__(self):
        parser = argparse.ArgumentParser(description='Download dos dados do Estado da Paraíba diponíveis em: http://dados.pb.gov.br/')
        parser.add_argument('-m','--merge',
                            help='Unir todos os arquivos', action='store_true')
        parser.add_argument('-f', '--format', 
                            help='Escolher formato de saída dos arquivos', type=str,
                            choices=['csv', 'json'], default='csv')
        parser.add_argument('month', help='Mês da pesquisa', type=int)
        parser.add_argument('year', help='Ano da pesquisa', type=int)
        parser.add_argument('--untilmonth', help='Mês final da pesquisa', type=int, default=0)
        parser.add_argument('--untilyear', help='Ano final da pesquisa', type=int, default=0)
        parser.add_argument('--db', help='Gerar arquivo .db', action='store_true')
        self.args = parser.parse_args()
    
    def get_args(self):
        return self.args