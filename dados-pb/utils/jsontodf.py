import os
import pandas as pd


def json_to_df(file_name, data):
    df = None

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data.decode('utf-8'))

    df = pd.read_json(file_name)
    os.remove(file_name)

    return df
