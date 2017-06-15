# -*- coding: utf-8 -*-
# generate_caffe_train_file.py - Removes the header from annotations.csv file in the train directory

import csv
import os

############
#
# TIANCHI CSV
TIANCHI_train_path = "/home/jenifferwu/TIANCHI/csv/train/"
TIANCHI_train_annotations = TIANCHI_train_path + "annotations.csv"
TIANCHI_train_seriesuids = TIANCHI_train_path + "seriesuids.csv"

output_path = "/home/jenifferwu/Caffe_CNN_Data/"
train_file = "train.txt"

#####################

# Read the annotations CSV file in (skipping first row).
csvRows = []
csvFileObj = open(TIANCHI_train_annotations)
readerObj = csv.reader(csvFileObj)
for row in readerObj:
    if readerObj.line_num == 1:
        continue    # skip first row
    csvRows.append(row)
    # csvRows.append(row['seriesuid'])
    # csvRows.append(row['diameter_mm'])
csvFileObj.close()


# Write out the train.txt CSV file.
csvFileObj = open(os.path.join(output_path, train_file), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    print row
    csvWriter.writerow(row)
csvFileObj.close()
