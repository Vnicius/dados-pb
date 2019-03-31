import os
import pandas as pd


def csv_to_df(file_name, csv_data):
    '''
        Salva um arquivo .csv e retorna um dataframe

        Params:
            file_name (str): nome do arquivo .csv
            csv_data (str): dados no farmato de csv
        
        Returns:
            (DataFrame): objeto DataFrame com os dados
    '''
    df = None

    # salvar o arquivo
    with open(file_name, 'w', encoding='utf-8') as f:
        try:
            f.write(csv_data.decode('utf-8'))
        except UnicodeDecodeError:
            f.write(csv_data.decode('latin-1'))

    # ler como dataframe
    df = pd.read_csv(file_name, sep=';')
    
    # remover arquivo
    os.remove(file_name)

    return df
