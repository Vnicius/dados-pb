# Dados PB

Scripts para realizar o download dos dados abertos do estado da Paraíba disponíveis em https://dados.pb.gov.br/

## Conteúdo

- CGE
- FOPAG
- SIAF
- SIGA

## Instalação

### Python 3.7

### PIP

```
  $ sudo pip install -r requirements.txt
```

### Anaconda

#### 1 - Criar o ambiente a partir do `env.yml`

```
  $ conda env create -f env.yml
```

#### 2 - Ativar o ambiente

```
  $ conda activate dados-pb
```

## Uso

```
usage: run.py [-h] [-m] [-f {csv,json}] [--untilmonth UNTILMONTH]
              [--untilyear UNTILYEAR] [--db] [-o OUTPUT]
              month year

Download dos dados do Estado da Paraíba diponíveis em: http://dados.pb.gov.br/

positional arguments:
  month                 mês dos documentos
  year                  ano dos documentos

optional arguments:
  -h, --help            show this help message and exit
  -m, --merge           unir todos os arquivos
  -f {csv,json}, --format {csv,json}
                        escolher formato de saída dos arquivos
  --untilmonth UNTILMONTH
                        mês final dos documentos
  --untilyear UNTILYEAR
                        ano final dos documentos
  -o OUTPUT, --output OUTPUT
                        diretório de saída
```

## Exemplos

- 1 - Realizar o download dos documentos em `.csv` referentes ao período de 02/2019

```
  $ cd src
  $ python run.py 2 2019
```

- 2 - Realizar o download dos documentos em `.json` referentes ao perído de 02/2018 a 02/2018

```
  $ cd src
  $ python run.py 2 2018 --untilmonth 2 --untilyear 2019 -f json
```
