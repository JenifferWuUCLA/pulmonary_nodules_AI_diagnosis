# -*- coding: utf-8 -*-
# create_TIANCHI_test_annotations.py - just keep 3 slices

from __future__ import print_function, division
import os
import csv
from glob import glob

try:
    from tqdm import tqdm  # long waits are not fun
except:
    print('TQDM does make much nicer wait bars...')
    tqdm = lambda x: x

############
#
# Getting list of image files
subset = "test_subset00/"
# subset = "subset3/"
tianchi_path = "/media/ucla/32CC72BACC727845/tianchi/"
# tianchi_path = "/home/jenifferwu/LUNA2016/"
tianchi_subset_path = tianchi_path + subset

output_path = "/media/ucla/32CC72BACC727845/tianchi/csv/test/"
# output_path = "/home/jenifferwu/LUNA2016/test/"

file_list = glob(tianchi_subset_path + "*.mhd")

csvRows = []


#####################
#
# Helper function to get rows in data frame associated
# with each file
def get_filename(file_list, case):
    for f in file_list:
        if case in f:
            return (f)


def csv_row(seriesuid, coordX, coordY, coordZ, diameter_mm):
    new_row = []
    new_row.append(seriesuid)
    new_row.append(coordX)
    new_row.append(coordY)
    new_row.append(coordZ)
    new_row.append(diameter_mm)
    csvRows.append(new_row)


#####
csv_row("seriesuid", "coordX", "coordY", "coordZ", "diameter_mm")

# Search the CT .mhd image list in test_subset folder
image_list = os.listdir(tianchi_subset_path)
for image in image_list:
    if ".mhd" not in image:
        continue
    seriesuid = image.replace(".mhd", "")
    csv_row(seriesuid, 0.0, 0.0, 0.0, 0.0)

# Re-Write out the annotations.txt CSV file.
csvFileObj = open(os.path.join(output_path, "annotations.csv"), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    # print row
    csvWriter.writerow(row)
csvFileObj.close()
