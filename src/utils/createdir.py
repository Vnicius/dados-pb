import os

def createdir(path):
    '''
        Cria um diretório se ele não existir

        Params:
            path (str): caminho do diretório
    '''
    try:
        os.mkdir(path)
    except:
        pass