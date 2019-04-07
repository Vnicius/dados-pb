import os
import glob
from datetime import datetime as dt
from dadospb.utils.DownloadArgs import DownloadArgs
import importlib

IGNORE_FILES = [os.path.join('dadospb', '__init__.py')]

def main(args):
    '''
        Executa os scripts de download

        Params:
            args: argumentos
    '''

    # buscar todos os arquivos .py
    files = glob.glob(os.path.join('dadospb','*.py'))
    files = [ f for f in files if not f in IGNORE_FILES ]
    
    # definir o diretôrio de saída
    if not args.output:
        args.output = f'data_{dt.now().strftime("%d-%m-%Y")}'

    # executar os scripts
    for f in files:
        module_name = f.replace('.py', '')
        module_name = '.'.join(os.path.split(module_name))
        module = importlib.import_module(module_name)
        module.Download(args).download()

if __name__ == '__main__':
    dargs = DownloadArgs()
    args = dargs.get_args()
    main(args)