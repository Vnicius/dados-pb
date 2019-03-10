import os
import pandas as pd


def json_to_df(file_name, json_data):
    '''
        Salva um arquivo .json e retorna um dataframe

        Params:
            file_name (str): nome do arquivo .json
            json_data (str): dados no farmato de json
        
        Returns:
            (DataFrame): objeto DataFrame com os dados
    '''

    df = None

    # salvar arquivo
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json_data.decode('utf-8'))

    # ler arquivo como dataframe
    df = pd.read_json(file_name)
    
    # remover arquivo
    os.remove(file_name)

    return df
