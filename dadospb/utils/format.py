def format_month(month):
    '''
        Formata o número do mês

        Params:
            month (int): mês em número
        
        Returns:
            (str): mês formatado em string
    '''
    if month < 10:
        return "0" + str(month)

    return str(month)

def format_period(start_month, start_year, end_month, end_year):
    '''
        Formatar o perído de consulta em string

        Params:
            start_month (int): valor do mês inicial
            start_year (int): valor do ano inicial
            end_month (int): valor do mês final
            end_year (int): valor do mês final
        
        Returns:
            (string): string formatada

    '''
    if start_month == end_month and start_year == end_year:
        return f'{format_month(start_month)}{start_year}'
    else:
        return f'{format_month(start_month)}{start_year}_{format_month(end_month)}{end_year}'