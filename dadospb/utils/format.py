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
        return f'{start_month:0>2d}{start_year}'
    return f'{start_month:0>2d}{start_year}_{end_month:0>2d}{end_year}'