# -*- coding: utf-8; -*-
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
