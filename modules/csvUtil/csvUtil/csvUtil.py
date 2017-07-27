#!/usr/bin/env python
#
#
#
"""
This module program performs common functions with csv files
"""

import csv
import os

def csvImport(filename, header=None):
    data = []

    with open(filename, 'rb') as fid:
        reader = csv.DictReader(fid, fieldnames=header)

        for row in reader:
            data.append(row)

    return reader.fieldnames, data


def csvExport(filename, headers, data):

    with open(filename, 'wb') as fid:
        writer = csv.DictWriter(fid, fieldnames=headers)

        writer.writeheader()
        writer.writerows(row)


if __name__ == '__main__':
    pass
