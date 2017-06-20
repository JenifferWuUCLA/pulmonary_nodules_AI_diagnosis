# -*- coding: utf-8 -*-
# generate_caffe_synset_words_file.py

import csv
import os

############
#

output_path = "/home/ucla/Downloads/Caffe_CNN_Data/"
synsets_file = "synset_words.txt"

csvRows = []


#####################
def csv_row(synsets, words):
    new_row = []
    new_row.append(synsets)
    new_row.append(words)
    csvRows.append(new_row)

#####################

csv_row('n01440010', 'It is not a real lung nodule.')
csv_row('n01440011', 'It is a real lung nodule.')

# Write out the train.txt CSV file.
csvFileObj = open(os.path.join(output_path, synsets_file), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    # print row
    csvWriter.writerow(row)
csvFileObj.close()
