#!/usr/bin/env python

from __future__ import print_function

import pandas as pd

if __name__=="__main__":
    frame = pd.read_csv('./country_rank.tsv', sep='\t')
    frame = frame.tail(1)
    dato = frame.dato.values[0]
    print("dato:", dato)
    columns = [(col, int(frame[col].values[0])) for col in frame.columns if col != 'dato']
    columns = sorted(columns, key=lambda x: x[1])
    for (k, v) in columns:
        print(k+':', v)

