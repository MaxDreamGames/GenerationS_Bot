countries_dict = {
    'Россия': 'RUS',
    'США': 'USA',
    'Китай': 'CHN',
    'Индия': 'IND',
    'Япония': 'JPN',
    'Германия': 'DEU',
    'Великобритания': 'GBR',
    'Франция': 'FRA',
    'Италия': 'ITA',
    'Бразилия': 'BRA',
    'Канада': 'CAN',
    'Южная Корея': 'KOR',
    'Австралия': 'AUS',
    'Испания': 'ESP',
    'Мексика': 'MEX',
    'Индонезия': 'IDN',
    'Нидерланды': 'NLD',
    'Турция': 'TUR',
    'Украина': 'UKR',
    'Польша': 'POL',
    'Саудовская Аравия': 'SAU',
    'Египет': 'EGY',
    'Аргентина': 'ARG',
    'Иран': 'IRN',
    'Нигерия': 'NGA',
    'Пакистан': 'PAK',
    'Колумбия': 'COL',
    'Бангладеш': 'BGD',
    'Филиппины': 'PHL',
    'Вьетнам': 'VNM',
    'Мозамбик': 'MOZ',
    'ЮАР': 'ZAF',
    'Румыния': 'ROU',
    'Кения': 'KEN',
    'Судан': 'SDN',
    'Мали': 'MLI',
    'Чехия': 'CZE',
    'Греция': 'GRC',
    'Израиль': 'ISR',
    'Гана': 'GHA',
    'Эфиопия': 'ETH',
    'Тунис': 'TUN',
    'Новая Зеландия': 'NZL',
    'Словения': 'SVN',
    'Болгария': 'BGR',
    'Уганда': 'UGA',
    'Эквадор': 'ECU',
    'Афганистан': 'AFG',
    'Венесуэла': 'VEN',
    'Куба': 'CUB',
    'Швейцария': 'CHE',
    'Малайзия': 'MYS',
    'Ливия': 'LBY',
    'Коста-Рика': 'CRI',
    'Сирия': 'SYR',
    'Чили': 'CHL',
    'Зимбабве': 'ZWE',
    'Непал': 'NPL',
    'Мадагаскар': 'MDG',
    'Республика Конго': 'COG',
    'Кот-д\'Ивуар': 'CIV',
    'Камерун': 'CMR',
    'Австрия': 'AUT',
    'Катар': 'QAT',
    'Сербия': 'SRB',
    'Алжир': 'DZA',
    'Ливан': 'LBN',
    'Узбекистан': 'UZB',
    'Грузия': 'GEO',
    'Гондурас': 'HND',
    'Тринидад и Тобаго': 'TTO',
    'Гонконг': 'HKG',
    'Доминиканская Республика': 'DOM',
    'Боливия': 'BOL',
    'Парагвай': 'PRY',
    'Сенегал': 'SEN',
    'Мьянма': 'MMR'
}

def check_country(country):
    if country in countries_dict:
        return countries_dict[country]
    else:
        return None