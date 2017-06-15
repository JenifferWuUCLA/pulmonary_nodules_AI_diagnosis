# -*- coding: utf-8 -*-
# generate_caffe_val_file.py - Removes the header from annotations.csv file in the val directory

import csv
import os

############
#
# TIANCHI CSV
TIANCHI_train_path = "/home/jenifferwu/TIANCHI/csv/val/"
TIANCHI_train_annotations = TIANCHI_train_path + "annotations.csv"
TIANCHI_train_seriesuids = TIANCHI_train_path + "seriesuids.csv"

output_path = "/home/jenifferwu/Caffe_CNN_Data/"
train_file = "val.txt"

csvRows = []


#####################
def csv_row(seriesuid, diameter_mm, nodule_class):
    new_row = []
    new_row.append(seriesuid)
    new_row.append(diameter_mm)
    new_row.append(nodule_class)
    csvRows.append(new_row)


def is_nodule(diameter_mm):
    # ０：不是真正肺结节；１：是真正肺结节。
    nodule_class = 0
    # print float(diameter_mm)
    # print float(diameter_mm) >= 10
    if float(diameter_mm) >= 10:
        nodule_class = 1
    return nodule_class


#####################

# Read the annotations CSV file in (skipping first row).

csvFileObj = open(TIANCHI_train_annotations)
readerObj = csv.DictReader(csvFileObj)

csv_row('seriesuid', 'diameter_mm', 'nodule_class')
for row in readerObj:
    if readerObj.line_num == 1:
        continue  # skip first row

    csv_row(row['seriesuid'], row['diameter_mm'], is_nodule(row['diameter_mm']))

csvFileObj.close()


# Write out the val.txt CSV file.
csvFileObj = open(os.path.join(output_path, train_file), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    # print row
    csvWriter.writerow(row)
csvFileObj.close()
