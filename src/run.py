import os
import glob
from datetime import datetime as dt
from utils.DownloadArgs import DownloadArgs

IGNORE_FILES = ['__init__.py', 'run.py']

def main(args):
    '''
        Executa os scripts de download

        Params:
            args: argumentos
    '''

    # buscar todos os arquivos .py
    files = glob.glob('*.py')
    files = [ f for f in files if not f in IGNORE_FILES ]
    
    # definir o diretôrio de saída
    if not args.output:
        args.output = f'data_{dt.now().strftime("%d-%m-%Y")}'

    # executar os scripts
    for f in files:
        module_name = f.replace('.py', '')
        module = __import__(module_name)
        module.Download(args).download()

if __name__ == '__main__':
    dargs = DownloadArgs()
    args = dargs.get_args()
    main(args)