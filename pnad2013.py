# -*- coding: utf-8; -*-

import io
import sys
import pandas

CONVERT_TABLE = {c: lambda value: int(value or 0) for c in [
    'V4746',
    'V4747',
    'V4748',
    'V4749',
]}

REGIOES_TABLE = {
    # 11	Rondônia
    # 12	Acre
    # 13	Amazonas
    # 14	Roraima
    # 15	Pará
    # 16	Amapá
    # 17	Tocantins
    # 21	Maranhão
    # 22	Piauí
    # 23	Ceará
    # 24	Rio Grande do Norte
    # 25	Paraíba
    # 26	Pernambuco
    # 27	Alagoas
    # 28	Sergipe
    # 29	Bahia
    # 31	Minas Gerais
    # 32	Espírito Santo
    # 33	Rio de Janeiro
    # 35	São Paulo
    # 41	Paraná
    # 42	Santa Catarina
    # 43	Rio Grande do Sul
    # 50	Mato Grosso do Sul
    # 51	Mato Grosso
    # 52	Goiás
    # 53	Distrito Federal
    'norte':        [11, 12, 13, 14, 15, 16, 17],
    'nordeste':     [21, 22, 23, 24, 25, 26, 27, 28, 29],
    'sul':          [41,42, 43],
    'centro-oeste': [50, 51, 52, 53],
    'sp':           [35],
    'rj':           [33],
    'mg':           [31],
    'es':           [32],
    'brasil':       [88],
    'estrangeiro':  [98],
}


IDADES_TABLE = {
    'ate 19':       [('lt', 20)],
    '20 a 39 anos': [('gte', 20), ('lt', 39)],
    'mais de 40':   [('gte', 40)],
}

CLASSES_TABLE = {
    'Ate 1SM':       [('lt', 789)],
    'De 1 a 2 SM':   [('gte', 789), ('lt', 1576)],
    'De 2 a 3SM':    [('gte', 1577), ('lt', 2364)],
    'De 3 a 5SM':    [('gte', 2365), ('lt', 3940)],
    'De 5 a 10SM':   [('gte', 3941), ('lt', 7880)],
    'De 10 a 20SM':  [('gte', 7881), ('lt', 15760)],
    'Acima de 20SM': [('gte', 15760)],
}


def filtrar_regiao(pnad, name):
    all_codes = REGIOES_TABLE[name][:]   # Do not touch actual value
    flag = (pnad.UF == all_codes.pop(0)) # Initialize flag
    for uf_id in REGIOES_TABLE[name]:
        flag |= (pnad.UF == uf_id)
    return flag


def filtrar_range(pnad, name, table, variable_name):
    all_ranges = table[name][:]   # Do not touch actual value
    variable = getattr(pnad, variable_name)
    operators = {
        'lt':  lambda v: (variable < v),
        'gte': lambda v: (variable >= v),
    }

    # Initialize flag
    initial_flag_data = all_ranges.pop(0)
    operator, value = initial_flag_data
    flag = operators[operator](value)

    # Add more flags
    for item in all_ranges:
        operator, value = item
        flag &= operators[operator](value)
    return flag


def filtrar_idade(pnad, name):
    return filtrar_range(pnad, name, table=IDADES_TABLE, variable_name='V8005')


def filtrar_classe(pnad, name):
    return filtrar_range(pnad, name, table=CLASSES_TABLE, variable_name='V4722')


def read_file(path):
    pnad = pandas.read_csv(
        path, sep=',', header=0, low_memory=False,
        converters=CONVERT_TABLE)

    ## Build a CSV manually. Let's start from the header
    print(','.join(['regiao', 'faixa etaria', 'renda', 'n', 'peso', 'n * peso']))

    ## The CSV body will be built here
    for regiao in REGIOES_TABLE:
        view = pnad[filtrar_regiao(pnad, regiao)]
        for idade in IDADES_TABLE:
            idade_view = view[filtrar_idade(view, idade)]
            for classe in CLASSES_TABLE:
                classe_view = idade_view[filtrar_classe(idade_view, classe)]
                weight = classe_view.mean()['V4729']
                count = len(classe_view)

                line = [regiao, idade, classe, count, weight, count * weight]
                print(','.join(str(l) for l in line))

if __name__ == '__main__':
    try:
        read_file(sys.argv[1])
    except IndexError:
        print("Usage: {0} dataset.csv".format(sys.argv[0]))
