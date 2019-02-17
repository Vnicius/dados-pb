import os
import requests as req
from datetime import datetime as dt
from utils.createdir import createdir
from utils.csvtodf import csv_to_df

TIME_NOW = dt.now()


class DownloadTemplate():
    def __init__(self,
                 base_url,
                 file_name,
                 file_type='csv',
                 start_year=2000,
                 start_month=1,
                 end_year=TIME_NOW.year,
                 end_month=TIME_NOW.month,
                 only_year=False):

        self.base_url = base_url
        self.file_name = file_name
        self.file_type = file_type.lower()
        self.start_year = start_year
        self.start_month = start_month
        self.end_year = end_year
        self.end_month = end_month
        self.only_year = only_year

    def get_url(self, year, month):
        raise NotImplementedError

    def preprocess(self, df):
        raise NotImplementedError

    def download(self):
        if self.start_year == TIME_NOW.year and self.start_month == TIME_NOW.month:
            if TIME_NOW.month == 1:
                self.start_year = self.start_year - 1
                self.start_month = 12
            else:
                self.start_month = self.start_month - 1

        createdir('data')

        for y in range(self.start_year, self.end_year + 1):
            createdir(os.path.join('data', str(y)))
            if not self.only_year:
                for m in range(self.start_month, self.end_month + 1):
                    path = os.path.join('data', str(y), str(m))
                    createdir(path)
                    csv_data = req.get(self.get_url(y, m)).content
                    self.__save(path, csv_data)

            else:
                data = req.get(self.get_url(y, 0)).content
                self.__save(os.path.join('data', str(y)), data)

    def __save(self, path, data):
        params = {'encoding': 'utf-8', 'sep': ';', 'index':
                  False}
        df = csv_to_df(
            os.path.join(path, f'{self.file_name}.{self.file_type}'), data)
        df = self.preprocess(df)

        df.to_csv(os.path.join(
            path, f'{self.file_name}.{self.file_type}'), **params)
