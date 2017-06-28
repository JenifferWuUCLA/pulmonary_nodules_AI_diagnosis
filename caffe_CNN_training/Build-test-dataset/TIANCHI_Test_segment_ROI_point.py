# usage: python TIANCHI_Test_segment_ROI_point.py

import numpy as np
import pickle
from skimage import measure
from glob import glob
import os
import csv

# subset = "train_dataset/"
subset = "data_set/"
# working_path = "/home/ucla/Downloads/tianchi/" + subset
# working_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset + "predictions/"
working_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset

# output_path = "/home/ucla/Downloads/Caffe_CNN_Data/"
output_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset + "predictions/"
ROI_point_file = "ROI_point.txt"

csvRows = []


def csv_row(avgEcc, avgEquivlentDiameter, stdEquivlentDiameter, weightedX, weightedY, numNodes, numNodesperSlice):
    new_row = []
    new_row.append(avgEcc)
    new_row.append(avgEquivlentDiameter)
    new_row.append(stdEquivlentDiameter)
    new_row.append(weightedX)
    new_row.append(weightedY)
    new_row.append(numNodes)
    new_row.append(numNodesperSlice)
    csvRows.append(new_row)


def getRegionFromMap(slice_npy):
    # print("getRegionFromMap slice_npy: %s" % (str(slice_npy)))
    thr = np.where(slice_npy > np.mean(slice_npy), 0., 1.0)
    label_image = measure.label(thr)
    labels = label_image.astype(int)
    regions = measure.regionprops(labels)
    return regions


def getRegionMetricRow(fname="nodules.npy"):
    csv_row("avgEcc", "avgEquivlentDiameter", "stdEquivlentDiameter", "weightedX", "weightedY", "numNodes",
            "numNodesperSlice")
    # fname, numpy array of dimension [#slices, 1, 512, 512] containing the images
    # file_list = glob(working_path + "imgs_mask_test_*.npy")
    file_list = glob(working_path + "images_*.npy")
    # file_list = glob(working_path + "masksTestPredicted.npy")
    for img_file in file_list:
        print("img_file: %s" % img_file)
        imgs_to_process = np.load(img_file).astype(np.float64)
        print(len(imgs_to_process))
        # fname = working_path + "predictions/masksTestPredicted.npy"
        # fname = np.load(fname)
        seg = imgs_to_process[0]
        nslices = seg.shape[0]
        # print("nslices: %s" % (str(nslices)))

        # metrics
        totalArea = 0.
        avgArea = 0.
        maxArea = 0.
        avgEcc = 0.
        avgEquivlentDiameter = 0.
        stdEquivlentDiameter = 0.
        weightedX = 0.
        weightedY = 0.
        numNodes = 0.
        numNodesperSlice = 0.
        # crude hueristic to filter some bad segmentaitons
        # do not allow any nodes to be larger than 10% of the pixels to eliminate background regions
        maxAllowedArea = 0.10 * 512 * 512

        areas = []
        eqDiameters = []
        for slicen in range(nslices):
            # print("slicen: %s" % (str(slicen)))
            # print("seg[slicen, 0, :, :]: %s" % (str(seg[0, 0, :, :])))
            print(seg)
            print(slicen)
            print(seg[slicen, 0, :, :])
            regions = getRegionFromMap(seg[slicen, 0, :, :])
            # print("regions: %s" % (str(regions)))
            for region in regions:
                # print("region: %s" % (str(region)))
                print("region.area: %s" % (str(region.area)))
                print("maxAllowedArea: %s" % (str(maxAllowedArea)))
                if region.area > maxAllowedArea:
                    print("region.area > maxAllowedArea: %s" % (str(region.area > maxAllowedArea)))
                    continue
                totalArea += region.area
                # print("totalArea: %s" % (str(totalArea)))
                areas.append(region.area)
                avgEcc += region.eccentricity
                avgEquivlentDiameter += region.equivalent_diameter
                eqDiameters.append(region.equivalent_diameter)
                weightedX += region.centroid[0] * region.area
                weightedY += region.centroid[1] * region.area
                numNodes += 1

        weightedX = weightedX / totalArea
        weightedY = weightedY / totalArea
        avgArea = totalArea / numNodes
        avgEcc = avgEcc / numNodes
        avgEquivlentDiameter = avgEquivlentDiameter / numNodes
        stdEquivlentDiameter = np.std(eqDiameters)

        maxArea = max(areas)

        numNodesperSlice = numNodes * 1. / nslices

        print(avgEcc, avgEquivlentDiameter, stdEquivlentDiameter, weightedX, weightedY, numNodes, numNodesperSlice)

        csv_row(avgEcc, avgEquivlentDiameter, stdEquivlentDiameter, weightedX, weightedY, numNodes, numNodesperSlice)

        # return np.array([avgArea, maxArea, avgEcc, avgEquivlentDiameter, stdEquivlentDiameter, weightedX, weightedY, numNodes, numNodesperSlice])


if __name__ == "__main__":
    getRegionMetricRow()

    # Write out the train.txt CSV file.
    csvFileObj = open(os.path.join(output_path, ROI_point_file), 'w')
    csvWriter = csv.writer(csvFileObj)
    for row in csvRows:
        # print row
        csvWriter.writerow(row)
    csvFileObj.close()
