# -*- coding: utf-8 -*-
import os

import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import SITKlib


def process_image(file_name, output_path, nodule):
    itk_img = sitk.ReadImage(file_name)
    # load the data once
    img_array = sitk.GetArrayFromImage(itk_img)  # indexes are z,y,x (notice the ordering)
    num_z, height, width = img_array.shape  # heightXwidth constitute the transverse plane
    origin = np.array(itk_img.GetOrigin())  # x,y,z  Origin in world coordinates (mm)
    spacing = np.array(itk_img.GetSpacing())  # spacing of voxels in world coor. (mm)
    # go through all nodes (why just the biggest?)
    node_x = nodule.node_x
    node_y = nodule.node_y
    node_z = nodule.node_z
    diam = nodule.diam
    # just keep 3 slices
    imgs = np.ndarray([3, height, width], dtype=np.float32)
    masks = np.ndarray([3, height, width], dtype=np.uint8)
    center = np.array([node_x, node_y, node_z])  # nodule center
    v_center = SITKlib.worldToVoxel(center, origin, spacing)  # nodule center in voxel space (still x,y,z ordering)
    for i, i_z in enumerate(np.arange(int(v_center[2]) - 1, int(v_center[2]) + 2).clip(0, num_z - 1)):
        # clip prevents going out of bounds in Z
        mask = SITKlib.make_mask(center, diam, i_z * spacing[2] + origin[2], width, height, spacing, origin)
        masks[i] = mask
        imgs[i] = img_array[i_z]
    np.save(os.path.join(output_path, "images.npy"), imgs)
    np.save(os.path.join(output_path, "masks.npy"), masks)
    SITKlib.show_img(imgs, masks)


def main():
    # Global Setting
    luna_path = "/home/jenifferwu/LUNA2016/"
    mhd_file_name = luna_path + 'subset0/1.3.6.1.4.1.14519.5.2.1.6279.6001.124154461048929153767743874565.mhd'
    # mhd_file_name = luna_path + 'subset4/1.3.6.1.4.1.14519.5.2.1.6279.6001.799582546798528864710752164515.mhd'
    tianchi_path = "/home/jenifferwu/TIANCHI/"
    # mhd_file_name = tianchi_path + 'train_subset00/LKDS-00001.mhd'

    output_path = "Huge CT Data"
    nodule = SITKlib.Nodule();

    '''
    nodule.node_x = 56.20840547
    nodule.node_y = 86.34341278
    nodule.node_z = -115.8675792
    nodule.diam = 23.35064438
    '''

    nodule.node_x = 145.967465
    nodule.node_y = -161.1976342
    nodule.node_z = -312.0713474
    nodule.diam = 6.378436317

    '''
    nodule.node_x = -128.3638897
    nodule.node_y = 53.10545586
    nodule.node_z = -142.1335065
    nodule.diam = 5.663498473
    '''

    '''
    nodule.node_x = -76.4498793983
    nodule.node_y = -49.5405710363
    nodule.node_z = 229.5
    nodule.diam = 14.1804045239
    '''

    process_image(mhd_file_name, output_path, nodule)


if __name__ == "__main__":
    main()
