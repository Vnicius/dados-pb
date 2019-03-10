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
    output_dir = ''

    if args.output_dir:
        output_dir = output_dir
    else:
        output_dir = f'data_{dt.now().strftime("%d-%m-%Y")}'

    # executar os scripts
    for f in files:
        module_name = f.replace('.py', '')
        module = __import__(module_name)
        module.Download(start_year=args.year, start_month=args.month,
             end_year=args.untilyear, end_month=args.untilmonth,
             merge_data=args.merge, file_type=args.format,
             output_dir=output_dir).download()

if __name__ == '__main__':
    dargs = DownloadArgs()
    args = dargs.get_args()
    main(args)