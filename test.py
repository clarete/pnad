# -*- coding: utf-8; -*-
import io
import convert
import sure


def test_get_var():
    "get_var() Should parse each field from a variable form a line"

    # Given the following line declaring one single variable
    line = "@00001          V0101          $4.          /*Ano de referência*/"

    # When the above line is parsed
    variable = convert.get_var(line)

    # Then it should be parsed into the following dictionary
    variable.should.equal({
        'position': 1,
        'size': 4,
        'name': 'V0101',
        'comment': 'Ano de referência',
    })


def test_get_vars():
    "get_vars() Should parse a data file using"

    # Given a file full of variables
    input_variables = """\
@00001          V0101          $4.          /*Ano de referência*/
@00005          UF          $2.          /*Unidade da Federação*/
@00005          V0102          $8.          /*Número de controle*/
@00013          V0103          $3.          /*Número de série*/
"""

    # When the get_vars function is applied
    variables = convert.get_vars(input_variables.splitlines())

    # Then it should return a list of dictionaries like this
    variables.should.equal([
        {'position': 1,
         'size': 4,
         'name': 'V0101',
         'comment': 'Ano de referência',
        },
        {'position': 5,
         'size': 2,
         'name': 'UF',
         'comment': 'Unidade da Federação',
        },
        {'position': 5,
         'size': 8,
         'name': 'V0102',
         'comment': 'Número de controle',
        },
        {'position': 13,
         'size': 3,
         'name': 'V0103',
         'comment': 'Número de série',
        },
    ])


def test_read_row():
    "read_row() "

    # Given the folowing variables
    variables = convert.get_vars("""\
@00001          V0101          $4.          /*Ano de referência*/
@00005          UF          $2.          /*Unidade da Federação*/
@00005          V0102          $8.          /*Número de controle*/
@00013          V0103          $3.          /*Número de série*/
@00016          V0301          $2.          /*Número de ordem*/
@00018          V0302          $1.          /*Sexo*/
@00019          V3031          $2.          /*Dia de nascimento*/
""".splitlines())

    line = """\
20141100001500101219081987027111414  2  170432  4           23     414       2041 18133     14                                                           1   1782560031                                                                                                                                           12 2       81234343           1000000001500              111132144120201                                     3 213                                                                                                 3434 43  434                                                                                                                4                                     09110132070812110107080000000015000000000015000000000015000000000015000000000015000203210025200252 4003000000000500033122100000000050020160623
"""

    values = convert.read_row(line, variables)

    values.should.equal([
        '2014', '11', '11000015', '001', '01', '2', '19',
    ])
