#!/usr/bin/env python
# -*- coding: utf-8; -*-
import io
import os
import sys


def get_var(line):
    # Read
    position, rest = line.split(' ', 1)
    variable, rest = rest.strip().split(' ', 1)
    size, rest = rest.strip().split(' ', 1)
    comment = rest.replace('/*', '').replace('*/', '').strip()

    # Convert
    position = int(position.replace('@', ''))
    variable = variable.strip()
    size = int(float(size.replace('$', '')))

    return {
        'name': variable,
        'position': position,
        'size': size,
        'comment': comment,
    }


def get_vars(varsfile):
    variables = []
    for line in varsfile:
        variable = get_var(line)
        variables.append(variable)
    return variables


def read_var(line, var):
    pos = var['position'] - 1   # 1 index based
    return line[pos : pos + var['size']]


def read_row(line, variables):
    columns = []
    for var in variables:
        value = read_var(line, var)
        columns.append(value.strip())
    return columns


def print_header(variables, separator):
    print(separator.join(x['name'].encode('utf-8') for x in variables))


def main(vars_file, data_file):
    vars_fp = io.open(vars_file)
    data_fp = io.open(data_file)
    variables = get_vars(vars_fp)
    separator = ','

    print_header(variables, separator)
    for line in data_fp:
        line = read_row(line, variables)
        print(separator.join(line))

    data_fp.close()
    vars_fp.close()

if __name__ == '__main__':
    main(*sys.argv[1:3])
