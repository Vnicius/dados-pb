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

#### 1 - Criar o ambiente a partir do `environment.yml`

```
  $ conda env create -n dados-pb -f environment.yml
```

#### 2 - Ativar o ambiente

```
  $ conda activate dados-pb
```

## Uso

```
usage: collect.py [-h] [-m] [-f {csv,json}] [--month MONTH] [--year YEAR]
                  [--untilmonth UNTILMONTH] [--untilyear UNTILYEAR] [--db]
                  [-o OUTPUT] [-d [DOCS [DOCS ...]]] [--list]

Download dos dados do Estado da Paraíba diponíveis em: http://dados.pb.gov.br/

optional arguments:
  -h, --help            show this help message and exit
  -m, --merge           unir todos os arquivos
  -f {csv,json}, --format {csv,json}
                        escolher formato de saída dos arquivos
  --month MONTH         mês dos documentos
  --year YEAR           ano dos documentos
  --untilmonth UNTILMONTH
                        mês final dos documentos
  --untilyear UNTILYEAR
                        ano final dos documentos
  --db                  gerar arquivo .db
  -o OUTPUT, --output OUTPUT
                        diretório de saída
  -d [DOCS [DOCS ...]], --docs [DOCS [DOCS ...]]
                        lista de documentos para realizar o download
  --list                listar todos os documentos
```

## Exemplos

- 1 - Realizar o download dos documentos em `.csv` referentes ao período de 02/2019

```
  $ python collect.py --month 2 --year 2019
```

- 2 - Realizar o download dos documentos em `.json` referentes ao perído de 02/2018 a 02/2019

```
  $ python collect.py --month 2 --year 2018 --untilmonth 2 --untilyear 2019 -f json
```

- 3 - Realizar o download de documentos específicos

```
  $ python collect.py --month 2 --year 2018 --untilmonth 2 --untilyear 2019 -f json --docs acao_governamental adm_escolar_indireta
```

## Documentos

- Ação Governamental - acao_governamental
- Administração Escolar Indireta - adm_escolar_indireta
- Administração Hospitalar Indireta - adm_hospitalar_indireta
- Categoria Econômica Despesa - categoria_economica_despesa
- Dotação Orçamentária - dotacao_orcamentaria
- Liquidação - liquidacao
- Tipo Modalidade de Pagamento - tp_modalidade_pagamento

## Notações

- un - Unidade
- cod - Código
- num - Número
- tp - tipo
- doc - documento
- dt - data
- desc - descrição
- org - organização
- obs - observação
- gp - grupo
