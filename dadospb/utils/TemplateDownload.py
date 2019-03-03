import os
import requests as req
from datetime import datetime as dt
import pandas as pd
import shutil
from utils.createdir import createdir
from utils.csvtodf import csv_to_df
from utils.jsontodf import json_to_df
from utils.format import format_month

TIME_NOW = dt.now()

class TemplateDownload():
    def __init__(self,
                 base_url,
                 file_name,
                 file_type='csv',
                 start_year=2000,
                 start_month=1,
                 end_year=0,
                 end_month=0,
                 only_year=False,
                 merge_data=False):

        self.base_url = base_url
        self.file_name = file_name
        self.file_type = file_type.lower()
        self.start_year = start_year
        self.start_month = start_month
        self.end_year = end_year
        self.end_month = end_month
        self.only_year = only_year
        self.merge_data = merge_data

    def get_url(self, year, month):
        raise NotImplementedError

    def preprocess(self, df):
        raise NotImplementedError

    def download(self):
        if self.end_year == 0 or self.end_month == 0:
            self.end_year = self.start_year
            self.end_month = self.start_month
        
        if self.start_year == TIME_NOW.year and self.start_month == TIME_NOW.month:
            if TIME_NOW.month == 1:
                self.start_year = self.start_year - 1
                self.start_month = 12
            else:
                self.start_month = self.start_month - 1

        if self.end_year == TIME_NOW.year and self.end_month == TIME_NOW.month:
            if TIME_NOW.month == 1:
                self.end_year = self.end_year - 1
                self.end_month = 12
            else:
                self.end_month = self.end_month - 1

        date_str = f'{format_month(self.start_month)}{self.start_year}_{format_month(self.end_month)}{self.end_year}'
        data_dir = f'data_{date_str}'
        tmp_dir = 'tmp'
        data_path = os.path.join(data_dir, self.file_name)
        data_tmp_path = os.path.join(data_dir, tmp_dir)
        datas = []

        createdir(data_dir)
        createdir(os.path.join(data_dir, tmp_dir))
        createdir(data_path)

        for y in range(self.start_year, self.end_year + 1):
            start = 1
            end = 12

            if y == self.start_year:
                start = self.start_month

            if y == self.end_year:
                end = self.end_month

            if not self.only_year:
                for m in range(start, end + 1):
                    data = req.get(self.get_url(y, m)).content
                    if self.merge_data:
                        datas.append(self.__get_df(
                            data_tmp_path, data, f'{self.file_name}_{y}{format_month(m)}'))
                    else:
                        self.__save(data_path, data,
                                    f'{self.file_name}_{y}{format_month(m)}')

            else:
                data = req.get(self.get_url(y, 0)).content

                if self.merge_data:
                    datas.append(self.__get_df(
                        data_tmp_path, data, f'{self.file_name}_{y}'))
                else:
                    self.__save(data_path, data, f'{self.file_name}_{y}')

        if self.merge_data:
            df = pd.concat(datas)
            self.__save_df(data_dir, df, self.file_name)

        shutil.rmtree(data_tmp_path)
        shutil.rmtree(data_path)

    def __save(self, path, data, file_name):
        df = self.__get_df(path, data, file_name)
        self.__save_df(path, df, file_name)

    def __save_df(self, path, df, file_name):
        params = {'encoding': 'utf-8', 'sep': ',', 'index': False}
        params_json = {'orient': 'records'}

        if self.file_type == 'csv':
            df.to_csv(os.path.join(
                path, f'{file_name}.{self.file_type}'), **params)

        elif self.file_type == 'json':
            df.to_json(os.path.join(
                path, f'{file_name}.{self.file_type}'), **params_json)

    def __get_df(self, path, data, file_name):
        df = {}
        if self.file_type == 'csv':
            df = csv_to_df(
                os.path.join(path, f'{file_name}.{self.file_type}'), data)

        elif self.file_type == 'json':
            df = json_to_df(os.path.join(
                path, f'{file_name}.{self.file_type}'), data)

        df = self.preprocess(df)

        return df
