#!/usr/bin/env python

import cowlogger
import pandas as pd
import os

path = os.getcwd()
filenames = os.listdir(path)

for file in filenames:
    fields = ['time', 'code']
    if file.endswith('.csv'):
        read = pd.read_csv(file, usecols=fields)
        read = read[read.time < 600]
        read = read.drop(read.tail(1).index)
        output = cowlogger.main(read)
        df = pd.DataFrame(output)
        filepath = path + '/output_csv/' + file
        print(filepath)
        export_csv = df.to_csv(path_or_buf=filepath, index=False, header=True)
