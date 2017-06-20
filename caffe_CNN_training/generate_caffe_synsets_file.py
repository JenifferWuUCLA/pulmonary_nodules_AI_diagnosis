# -*- coding: utf-8 -*-
# generate_caffe_synsets_file.py

import csv
import os

############
#

output_path = "/home/ucla/Downloads/Caffe_CNN_Data/"
synsets_file = "synsets.txt"

csvRows = []


#####################
def csv_row(synsets):
    new_row = []
    new_row.append(synsets)
    csvRows.append(new_row)

#####################

csv_row('n01440010')
csv_row('n01440011')

# Write out the train.txt CSV file.
csvFileObj = open(os.path.join(output_path, synsets_file), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    # print row
    csvWriter.writerow(row)
csvFileObj.close()
