from os import path
import glob
from datetime import datetime as dt
import json
from dadospb.utils.DownloadArgs import DownloadArgs
from dadospb.DataDownloader import DataDownloader

IGNORE_FILES = ['__init__']


def main(args):
    '''
        Executa os scripts de download

        Params:
            args: argumentos
    '''

    # definir o diretôrio de saída
    if not args.output:
        args.output = f'data_{dt.now().strftime("%d-%m-%Y")}'

    
    with open(path.abspath(path.join('.', 'data-config.json')), 'r', encoding='utf-8') as config_file:
        database_config = json.load(config_file)

        # executar os scripts
        for group in database_config:
            if args.list:
                print(group.upper())
                
            for data in database_config[group]:
                if args.list:
                    print(f'- {data["title"]} - {data["tag"]}')
                else:
                    if len(args.docs) > 0 and data['tag'] not in args.docs:
                        continue
                    
                    DataDownloader(data, args).download()


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
