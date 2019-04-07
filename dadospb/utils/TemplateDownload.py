import os
import requests as req
from requests.exceptions import ConnectionError
from datetime import datetime as dt
import pandas as pd
import shutil
from dadospb.utils.createdir import createdir
from dadospb.utils.csvtodf import csv_to_df
from dadospb.utils.jsontodf import json_to_df
from dadospb.utils.format import format_month
from halo import Halo
import logging

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
    '''

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
                 periodic_data=True):
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
        self.output_dir = output_dir
        self.periodic_data = periodic_data

        self.__spinner = Halo(text=f'Baixando {self.get_title()}', spinner='dots')

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
        if self.end_year == 0 or self.end_month == 0:
            self.end_year = self.start_year
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

    def __download_fixed_data(self):
        '''
            Realizar o download do arquivo sem período de tempo
        '''
        # iniciar o spinner
        self.__spinner_start()
        
        data_dir = self.output_dir # diretorio dos dados
        data = ''

        createdir(data_dir) # criar o diretório dos dados

        logging.basicConfig(filename=os.path.join(data_dir, f'log.log'),
                            level=logging.INFO, 
                            format='%(asctime)s: %(module)s: %(levelname)s: %(message)s')

        try:
            # realizar dowload dos dados
            logging.info(f'Baixando {self.get_url(0, 0)}')
            
            data = req.get(self.get_url(0, 0)).content

            logging.info(f'Baixado')
        except ConnectionError :
            logging.error(f'Erro ao baixar {self.get_url(0, 0)}')
            self.__spinner_fail()
            return
        
        # salvar o arquivo
        self.__save(data_dir, data, self.file_name)

        # finalizar o spinner
        self.__spinner_succeed()

    def __download_in_period(self):
        '''
            Realiza o download dos arquivos num dado perído de tempo
        '''

        # iniciar o spinner
        self.__spinner_start()

        # ajeitar o ano e o mês
        self.__fix_period()
        
        data_dir = self.output_dir # diretorio dos dados
        tmp_dir = 'tmp' # diretório temporário
        data_path = data_dir if self.__is_single_date() else os.path.join(data_dir, self.file_name) # caminho do arquivo
        data_tmp_path = os.path.join(data_dir, tmp_dir) # caminho do arquivo temporário
        datas = []  # lista de dados
        
        # criar o diretório dos dados
        createdir(data_dir)

        logging.basicConfig(filename=os.path.join(data_dir, f'log.log'),
                            level=logging.INFO, 
                            format='%(asctime)s: %(module)s: %(levelname)s: %(message)s')

        # criar o diretório temporário
        logging.info(f'Criando diretório "{os.path.join(data_dir, tmp_dir)}"')
        createdir(os.path.join(data_dir, tmp_dir)) 

        # cirar diretório para os arqivos baixados
        logging.info(f'Criando diretório "{data_path}"')
        createdir(data_path)

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
                        self.__spinner_fail()
                        return

                    if self.merge_data:
                        logging.info(f'Guardando os dados de "{self.file_name}_{y}{format_month(m)}"')
                        data_df = self.__get_df(
                            data_tmp_path, data, f'{self.file_name}_{y}{format_month(m)}')
                        
                        if data_df.empty:
                            logging.info(f'VAZIO: "{self.file_name}_{y}{format_month(m)}"')
                        else:
                            datas.append(data_df)
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
                    self.__spinner_fail()
                    return

                if self.merge_data:
                    logging.info(f'Guardando os dados de "{self.file_name}_{y}"')
                    data_df = self.__get_df(
                        data_tmp_path, data, f'{self.file_name}_{y}')

                    if data_df.empty:
                        logging.info(f'VAZIO: "{self.file_name}_{y}"')
                    else:
                        datas.append(data_df)
                else:
                    self.__save(data_path, data, f'{self.file_name}_{y}')

        # juntar os arquivos
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
        df = self.__get_df(path, data, file_name)

        if df.empty:
            logging.info(f'VAZIO: "{file_name}"')

        # salvar o arquivo
        self.__save_df(path, df, file_name)

    def __save_df(self, path, df, file_name):
        '''
            Salva um objeto DataFrame

            Params:
                path (str): caminho onde o arquivo deve ser salvo
                df (DataFrame): objeto DataFrame
                file_name (str): nome do arquivo
        '''
        
        logging.info(f'Salvando o arquivo "{file_name}" em "{path}"')

        # definir parâmetros de salvamento
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
        '''
            Adiquirir o objeto DataFrame a partir de um conjunto de dados

            Params:
                path (str): caminho onde o arquivo deve ser salvo
                data (str): conteúdo do arquivo
                file_name (str): nome do arquivo
        '''
        
        logging.info(f'Lendo {file_name}.{self.file_type}')

        df = pd.DataFrame()

        try:
            if self.file_type == 'csv':
                # ler csv
                df = csv_to_df(
                    os.path.join(path, f'{file_name}.{self.file_type}'), data)

            elif self.file_type == 'json':
                # ler json
                df = json_to_df(os.path.join(
                    path, f'{file_name}.{self.file_type}'), data)

            df = self.preprocess(df)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()

        return df
