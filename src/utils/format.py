def format_month(month):
    if month < 10:
        return "0" + str(month)

    return str(month)

def format_period(start_month, start_year, end_month, end_year):
    if start_month == end_month and start_year == end_year:
        return f'{format_month(start_month)}{start_year}'
    else:
        return f'{format_month(start_month)}{start_year}_{format_month(end_month)}{end_year}'