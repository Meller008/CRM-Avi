from re import findall


def str_to_date(date):
    year = findall(r'\d\d\d\d', date)
    month = findall(r'[-.](\d\d)[-.]', date)
    day = findall(r'[-.](\d\d)$', date)
    return year, month, day
