#!/usr/bin/env python
# -*- Coding: utf-8; -*-

import io
import os

def get_vars(filepath):
    variables = []
    total_size = 0
    varsfile = io.open(filepath)

    for line in varsfile:
        # Read
        position, rest = line.split(' ', 1)
        variable, rest = rest.strip().split(' ', 1)
        size, rest = rest.strip().split(' ', 1)
        comment = rest.replace('/*', '').replace('*/', '').strip()

        # Convert
        position = int(position.replace('@', ''))
        variable = variable.strip()
        size = int(float(size.replace('$', '')))

        variables.append({'name': comment, 'position': position, 'size': size})
        total_size += size

    varsfile.close()
    return total_size, variables

def read_var(fp, var, offset):
    fp.seek(offset + var['position'] - 1) # 1 index based
    return fp.read(var['size'])

def read_row(fp, variables, offset):
    columns = []
    for var in variables:
        value = read_var(fp, var, offset)
        columns.append(value.strip())
    return columns

def print_header(variables, separator):
    print(separator.join(x['name'].encode('utf-8') for x in variables))

def main(vars_file, data_file):
    data_fp = io.open(data_file)
    row_size, variables = get_vars(vars_file)
    total_row_number = os.stat(data_file).st_size / row_size
    row_count = 0

    separator = ','

    print_header(variables, separator)
    while row_count <= total_row_number:
        print(separator.join(read_row(data_fp, variables, row_size * row_count)))
        row_count += 1

    data_fp.close()

if __name__ == '__main__':
    main(sys.argv[1:3])
