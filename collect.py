from os import path
import glob
from datetime import datetime as dt
from dadospb.utils.DownloadArgs import DownloadArgs
import importlib

IGNORE_FILES = ['__init__']


def main(args):
    '''
        Executa os scripts de download

        Params:
            args: argumentos
    '''

    # buscar todos os arquivos .py
    files = glob.glob(path.join('dadospb', '*.py'))
    files = sorted(list(get_files(files, args.docs)))

    # definir o diretôrio de saída
    if not args.output:
        args.output = f'data_{dt.now().strftime("%d-%m-%Y")}'

    # executar os scripts
    for f in files:
        module_name = f.replace('.py', '')
        module_name = '.'.join(path.split(module_name))
        module = importlib.import_module(module_name)
        download_obj = module.Download(args)

        if args.list:
            print(f'- {download_obj.get_title()} - {module.FILE_NAME}')
        else:
            download_obj.download()


def get_files(files, priority_list=[]):
    '''
        Filtra os arquivos que serão baixados

        Params:
            files(list): lista com os arquivos
            priority_list(list): lista com os arquivos prioritários
    '''
    for f in files:
        file_name = path.split(f)[-1].replace('.py', '')

        if priority_list:
            if file_name in priority_list and\
                    file_name not in IGNORE_FILES:
                yield(f)
        elif file_name not in IGNORE_FILES:
            yield(f)


if __name__ == '__main__':
    dargs = DownloadArgs()
    args = dargs.get_args()
    main(args)
