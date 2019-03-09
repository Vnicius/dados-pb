import os
import requests as req
from requests.exceptions import ConnectionError
from datetime import datetime as dt
import pandas as pd
import shutil
from utils.createdir import createdir
from utils.csvtodf import csv_to_df
from utils.jsontodf import json_to_df
from utils.format import format_month
from halo import Halo
import logging

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
                 merge_data=False,
                 output_dir='data'):

        self.base_url = base_url
        self.file_name = file_name
        self.file_type = file_type.lower()
        self.start_year = start_year
        self.start_month = start_month
        self.end_year = end_year
        self.end_month = end_month
        self.only_year = only_year
        self.merge_data = merge_data
        self.output_dir = output_dir

    def get_title(self):
        raise NotImplementedError

    def get_url(self, year, month):
        raise NotImplementedError

    def preprocess(self, df):
        raise NotImplementedError
    
    def __fix_period(self):
        if self.end_year == 0 or self.end_month == 0:
            self.end_year = self.start_year
            self.end_month = self.start_month
        
        if self.start_year == self.end_year:
            if self.start_month > self.end_month:
                self.start_month, self.end_month = self.end_month, self.start_month
        elif self.start_year > self.end_year:
            self.start_year, self.end_year = self.end_year, self.start_year
            self.start_month, self.end_month = self.end_month, self.start_month
        
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

    def download(self):
        # iniciar o spinner
        spinner = Halo(text=f'Baixando {self.get_title()}', spinner='dots')
        spinner.start()

        # ajeitar o ano e o mês
        self.__fix_period()
        
        data_dir = self.output_dir # diretorio dos dados
        tmp_dir = 'tmp' # diretório temporário
        data_path = os.path.join(data_dir, self.file_name) # caminho do arquivo
        data_tmp_path = os.path.join(data_dir, tmp_dir) # caminho do arquivo temporário
        datas = []  # lista de dados
        
        createdir(data_dir) # criar o diretório dos dados

        logging.basicConfig(filename=os.path.join(data_dir, f'log.log'),
                            level=logging.INFO, 
                            format='%(asctime)s: %(module)s: %(levelname)s: %(message)s')


        logging.info(f'Criando diretório "{os.path.join(data_dir, tmp_dir)}"')
        createdir(os.path.join(data_dir, tmp_dir)) # criar o diretório temporário

        logging.info(f'Criando diretório "{data_path}"')
        createdir(data_path) # cirar diretório para os arqivos baixados

        for y in range(self.start_year, self.end_year + 1):
            start = 1
            end = 12

            if y == self.start_year:
                start = self.start_month

            if y == self.end_year:
                end = self.end_month

            # se os dados são mensais
            if not self.only_year:
                for m in range(start, end + 1):
                    # realizar o dowload dos dados
                    try:
                        # realizar dowload dos dados
                        logging.info(f'Baixando {self.get_url(y, m)}')
                        
                        data = req.get(self.get_url(y, m)).content

                        logging.info(f'Baixado')
                    except ConnectionError :
                        logging.error(f'Erro ao baixar {self.get_url(y, m)}')
                        spinner.fail(text=f'Erro ao baixar {self.get_title()}')
                        return

                    if self.merge_data:
                        logging.info(f'Guardando os dados de "{self.file_name}_{y}{format_month(m)}"')
                        datas.append(self.__get_df(
                            data_tmp_path, data, f'{self.file_name}_{y}{format_month(m)}'))
                    else:
                        self.__save(data_path, data,
                                    f'{self.file_name}_{y}{format_month(m)}')

            else:
                # se os dados são anuais
                try:
                    # realizar dowload dos dados
                    logging.info(f'Baixando {self.get_url(y, 0)}')
                    data = req.get(self.get_url(y, 0)).content
                except ConnectionError:
                    logging.error(f'Erro ao baixar {self.get_url(y, 0)}')
                    spinner.fail(text=f'Erro ao baixar {self.get_title()}')
                    return

                if self.merge_data:
                    logging.info(f'Guardando os dados de "{self.file_name}_{y}"')
                    datas.append(self.__get_df(
                        data_tmp_path, data, f'{self.file_name}_{y}'))
                else:
                    self.__save(data_path, data, f'{self.file_name}_{y}')

        # junstar os arquivos
        if self.merge_data:
            logging.info(f'Juntando os arquivos')
            df = pd.concat(datas)
            self.__save_df(data_dir, df, self.file_name)

        # remover a o diretório temporário
        logging.info(f'Removendo diretório temporário "{data_tmp_path}"')
        shutil.rmtree(data_tmp_path)
        
        # remover os diretório com os arquvios separados
        if self.merge_data:
            logging.info(f'Removendo diretório "{data_path}"')
            shutil.rmtree(data_path)
        
        # finalizar o spinner
        spinner.succeed(text=self.get_title())

    def __save(self, path, data, file_name):

        # pegar o dataframe
        df = self.__get_df(path, data, file_name)

        # salvar o arquivo
        self.__save_df(path, df, file_name)

    def __save_df(self, path, df, file_name):
        
        logging.info(f'Salvando o arquivo "{file_name}" em "{path}"')

        params = {'encoding': 'utf-8', 'sep': ',', 'index': False}
        params_json = {'orient': 'records'}

        if self.file_type == 'csv':
            # salvar csv
            df.to_csv(os.path.join(
                path, f'{file_name}.{self.file_type}'), **params)

        elif self.file_type == 'json':
            # salvar json
            df.to_json(os.path.join(
                path, f'{file_name}.{self.file_type}'), **params_json)
        
        logging.info(f'Arquivo "{file_name}" salvo em "{path}"')

    def __get_df(self, path, data, file_name):
        
        logging.info(f'Lendo {file_name}.{self.file_type}')

        df = {}

        if self.file_type == 'csv':
            # ler csv
            df = csv_to_df(
                os.path.join(path, f'{file_name}.{self.file_type}'), data)

        elif self.file_type == 'json':
            # ler json
            df = json_to_df(os.path.join(
                path, f'{file_name}.{self.file_type}'), data)

        df = self.preprocess(df)

        return df
