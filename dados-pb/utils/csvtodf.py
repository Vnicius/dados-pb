import os
import pandas as pd


def csv_to_df(file_name, csv_data):
    df = None

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(csv_data.decode('utf-8'))

    df = pd.read_csv(file_name, sep=';')
    os.remove(file_name)

    return df
