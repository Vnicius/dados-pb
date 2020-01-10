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
  --no-verify-ssl       ignorar certificados SSL
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

**CGE**

- Dotação Orçamentária - dotacao_orcamentaria
- Liquidação - liquidacao
- Tipo Modalidade de Pagamento - tp_modalidade_pagamento

**DADOS-PB**

- Ação Governamental - acao_governamental
- Administração Escolar Indireta - adm_escolar_indireta
- Administração Hospitalar Indireta - adm_hospitalar_indireta
- Categoria Econômica Despesa - categoria_economica_despesa
- Elemento da Despesa - elemento_despesa
- Fonte de Recurso - fonte_recurso
- Função - funcao
- Grupo Natureza de Despesa - gp_natureza_despesa
- Item da Despesa - item_despesa
- Modalidade Aplicação Despesa - modalidade_aplicacao_despesa
- Modalidade de Licitação - modalidade_licitacao
- Motivo da Dispensa de Licitação - motivo_dispensa_licitacao
- Programas - programas
- Subfunção - subfuncao
- Tipos de Orçamentos - tipos_orcamento
- Unidade Gestora - und_gestora
- Unidade Orçamentária - und_orcamentaria

**FOPAG**

- Resumo da Folha de Pagamento - resumo_folha_pagamento

**SIAF**

- Despesa Orçamentária: Notas de Empenho - notas_empenho
- Despesa Orçamentária: Notas de Empenho de Anulação - notas_empenho_anulacao
- Despesa Orçamentária: Notas de Empenho de Suplementação - notas_empenho_suplementacao
- Despesa Orçamentária: Notas de Empenho - Diárias - notas_empenho_diarias
- Despesas: Anulações de Autorização de Pagamento - anulacoes_pagamento
- Despesas: Autorizações de Pagamento - autorizacoes_pagamento
- Grupo Financeiro - gp_financeiro
- Receitas: Execução - receitas_execucao
- Receitas: Previsão - receitas_previsao
- Situação Empenho - situacao_empenho
- Tipo de Crédito - tp_credito
- Tipo de Movimentação Orçamentária - tp_movimentacao_orcamentaria
- Tipos de Documentos - tp_documentos

**SIGA**

- Contratos - contratos
- Contratos: Aditivos - contratos_aditivos
- Convênios: Aditivos - convenios_aditivos
- Convênios: Entre o Estado e os municípios - convenios_estados_municipios

## Notações

- und - Unidade
- cod - Código
- num - Número
- tp - tipo
- doc - documento
- dt - data
- desc - descrição
- org - organização
- obs - observação
- gp - grupo
