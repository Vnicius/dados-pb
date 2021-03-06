import logging
import os
import warnings
from datetime import datetime as dt
from functools import partial
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import requests
from halo import Halo
from requests.exceptions import ConnectionError


TIME_NOW = dt.now()


class TemplateDownload():
    '''
        Classe de template para realizar os downloads dos arquivos

        Attr:
            base_url (str): URL base para os downloads
            file_name (str): nome do arquivo
            file_type (str): tipo do arquivo a ser baixado
            start_year (int): ano inicial
            start_month (int): mês inicial
            end_year (int): ano final
            end_month (int): mês final
            only_year (bool): se o arquivo é anual
            merge_data (bool): se deve ser realizada a junção 
                de todos os arquivos do período
            output_dir (str): diretôrio de saída
            periodic_data (bool): se os dados são atualizados periodicamente
            no_verify_ssl (bool): se desconsidera veirificação de SSL
    '''
    PANDAS_READ_METHODS = {
        "csv": partial(pd.read_csv, sep=";"),
        "json": pd.read_json
    }

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
                 output_dir='data',
                 periodic_data=True,
                 no_verify_ssl=False):
        '''
            Construtor da classe TemplateDownload

            Params:
                base_url (str): URL base para os downloads
                file_name (str): nome do arquivo
                file_type (str): tipo do arquivo a ser baixado (default: "csv")
                start_year (int): ano inicial (default: 2000)
                start_month (int): mês inicial (default: 1)
                end_year (int): ano final (default: 0)
                end_month (int): mês final (default: 0)
                only_year (bool): se o arquivo é anual (default: False)
                merge_data (bool): se deve ser realizada a junção (default: False)
                    de todos os arquivos do período
                output_dir (str): diretôrio de saída (default: "data")
                periodic_data (bool): se os dados são atualizados periodicamente
                no_verify_ssl (bool): se desconsidera veirificação de SSL
        '''

        self.base_url = base_url
        self.file_name = file_name
        self.file_type = file_type.lower()
        self.start_year = start_year
        self.start_month = start_month
        self.end_year = end_year
        self.end_month = end_month
        self.only_year = only_year
        self.merge_data = merge_data
        self.output_dir = Path(output_dir)
        self.periodic_data = periodic_data
        self.verify_ssl = not no_verify_ssl

        self.output_dir.mkdir(exist_ok=True)
        self.output_sub_dir = None
        if not self.__is_single_date() and not self.merge_data:
            self.output_sub_dir = self.output_dir / self.file_name
            self.output_sub_dir.mkdir(exist_ok=True)

        self.pandas_read_method = self.PANDAS_READ_METHODS[self.file_type]
        self.__spinner = Halo(text=f'Baixando {self.get_title()}', spinner='dots')

        logging.basicConfig(filename=self.output_dir / 'log.log',
                            level=logging.INFO, 
                            format='%(asctime)s: %(module)s: %(levelname)s: %(message)s')

    def get_title(self):
        ''' 
            Retorna o título do módulo

            Returns:
                (str): título
        '''
        
        raise NotImplementedError

    def get_url(self, year, month):
        '''
            Retorna a URL formatada para um dado ano e mês

            Params:
                year (int): ano do arquivo
                month (int): mês do arquivo
            
            Returns:
                (str): URL formatada
        '''
        
        raise NotImplementedError

    def preprocess(self, df):
        '''
            Pré-processa o dataframe

            Params:
                df (DataFrame): objeto DataFrame atual
            
            Returns:
                (DataFrame): objeto DataFrama pré-processado
        '''

        raise NotImplementedError
    
    def __fix_period(self):
        ''' Conserta os valores do período de consulta '''

        # verifica se o perído final não foi definido        
        if self.end_year == 0:
            self.end_year = self.start_year
        
        if self.end_month == 0 and not self.only_year:
            self.end_month = self.start_month
        
        # verifica se o período final é anterior ao inicial
        if self.start_year == self.end_year:
            if self.start_month > self.end_month:
                self.start_month, self.end_month = self.end_month, self.start_month
        elif self.start_year > self.end_year:
            self.start_year, self.end_year = self.end_year, self.start_year
            self.start_month, self.end_month = self.end_month, self.start_month
        
        # verifica se o período final é igual ao mês/ano corrente
        # os dados do mês atual só são diponíveis no final do mesmo
        if self.end_year == TIME_NOW.year and self.end_month == TIME_NOW.month:
            if TIME_NOW.month == 1:
                self.end_year = self.end_year - 1
                self.end_month = 12
            else:
                self.end_month = self.end_month - 1

    def __spinner_start(self):
        '''
            Iniciar spinner
        '''

        self.__spinner.start()
    
    def __spinner_succeed(self):
        '''
            Parar spinner com mensagem de sucesso
        '''

        self.__spinner.succeed(text=self.get_title())
    
    def __spinner_fail(self):
        '''
            Parar spinner com mensagem de erro
        '''

        self.__spinner.fail(text=f'Erro ao baixar {self.get_title()}')
    
    def __is_single_date(self):
        '''
            Verifica se o download é de apenas um único mês/ano
        '''

        if (self.start_year == self.end_year and self.start_month == self.end_month) or self.end_year == self.end_month:
            return True
        
        return False

    def download(self):
        '''
            Realizar o download
        '''

        if self.periodic_data:
            self.__download_in_period()
        else:
            self.__download_fixed_data()

    def __load_data(self, year=0, month=0):
        url = self.get_url(year, month)
        logging.info(f'Baixando {url}')

        try:
            with warnings.catch_warnings():  # disable non-SSL warning if needed
                warnings.simplefilter("ignore")
                resp = requests.get(url, verify=self.verify_ssl)
        except ConnectionError :
            logging.error(f'Erro ao baixar {url}', exc_info=True)
            self.__spinner_fail()
            return False

        logging.info('Baixado')
        return resp.text

    def __download_fixed_data(self):
        '''
            Realizar o download do arquivo sem período de tempo
        '''
        self.__spinner_start()
        data = self.__load_data()
        if data is False:
            return

        self.__save(self.output_dir, data, self.file_name)
        self.__spinner_succeed()

    def __download_in_period(self):
        '''
            Realiza o download dos arquivos num dado perído de tempo
        '''
        self.__spinner_start()
        self.__fix_period()
        dataframes = []  # lista de dataframes

        with TemporaryDirectory() as tmp:
            for y in range(self.start_year, self.end_year + 1):
                start = self.start_month if y == self.start_year else 1
                end = self.end_month if y == self.end_year else 12

                # se os dados são mensais
                if not self.only_year:
                    for m in range(start, end + 1):
                        # realizar o dowload dos dados
                        data = self.__load_data(y, m)
                        if data is False:
                            return

                        if self.merge_data:
                            logging.info(f'Guardando os dados de "{self.file_name}_{y}{m:0>2d}"')
                            df = self.__get_df(data)
                            if df.empty:
                                logging.info(f'VAZIO: "{self.file_name}_{y}{m:0>2d}"')
                            else:
                                dataframes.append(df)

                        elif self.output_sub_dir:
                            self.__save(self.output_sub_dir, data, f'{self.file_name}_{y}{m:0>2d}')

                # se os dados são anuais
                else:
                    data = self.__load_data(y)
                    if data is False:
                        return

                    if self.merge_data:
                        logging.info(f'Guardando os dados de "{self.file_name}_{y}"')
                        df = self.__get_df(data)
                        if df.empty:
                            logging.info(f'VAZIO: "{self.file_name}_{y}"')
                        else:
                            dataframes.append(df)
                    elif self.output_sub_dir:
                        self.__save(self.output_sub_dir, data, f'{self.file_name}_{y}')

            # juntar os arquivos
            if self.merge_data and dataframes:
                logging.info(f'Juntando os arquivos')
                self.__save_df(self.output_dir, pd.concat(dataframes), self.file_name)

            # finalizar o spinner
            self.__spinner_succeed()

    def __save(self, path, data, file_name):
        '''
            Salva um arquivo

            Params:
                path (str): caminho onde o arquivo deve ser salvo
                data (str): conteúdo do arquivo
                file_name (str): nome do arquivo
        '''
        # pegar o dataframe
        df = self.__get_df(data)

        if df.empty:
            logging.info(f'VAZIO: "{file_name}"')

        # salvar o arquivo
        self.__save_df(path, df, file_name)

    def __save_df(self, path, df, file_name):
        '''
            Salva um objeto DataFrame

            Params:
                path (pathlib.Pah): caminho onde o arquivo deve ser salvo
                df (DataFrame): objeto DataFrame
                file_name (str): nome do arquivo
        '''
        

        # definir parâmetros de salvamento
        params = {
            'csv': {'encoding': 'utf-8', 'sep': ',', 'index': False},
            'json': {'orient': 'records'}
        }
        write_methods = {"csv": df.to_csv, "json": df.to_json}

        kwargs = params[self.file_type]
        write_method = write_methods[self.file_type]
        file_name = path / f'{file_name}.{self.file_type}'

        logging.info(f'Salvando o arquivo "{file_name}"')
        write_method(file_name, **kwargs)
        logging.info(f'Arquivo "{file_name}" salvo')

    def __get_df(self, data):
        '''
            Adiquirir o objeto DataFrame a partir de um conjunto de dados

            Params:
                data (str): conteúdo do arquivo
        '''
        with StringIO(data) as buffer:
            try:
                return self.preprocess(self.pandas_read_method(buffer))
            except pd.errors.EmptyDataError:
                return pd.DataFrame()
