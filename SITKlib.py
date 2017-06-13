# -*- coding: utf-8 -*-
import os

import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt


class Nodule:
    def __init__(self):
        self.node_x = 0
        self.node_y = 0
        self.node_z = 0
        self.diam = 0


def worldToVoxel(worldCoord, origin, spacing):
    '''
        结节世界坐标转成图像坐标
        worldCoord:结节世界坐标
        origin:边缘坐标
        spacing：比例尺
    '''
    voxelCoord = np.absolute(worldCoord - origin)
    voxelCoord = voxelCoord / spacing
    voxelCoord = voxelCoord.astype(np.int32)
    return voxelCoord


def show_img(imgs, masks):
    for i in range(len(imgs)):
        print ("图片的第 %d 层" % i)
        fig, ax = plt.subplots(2, 2, figsize=[8, 8])
        ax[0, 0].imshow(imgs[i])
        ax[0, 0].set_title(u'彩色切片')
        ax[0, 1].imshow(imgs[i], cmap='gray')
        ax[0, 1].set_title(u'黑白切片')
        ax[1, 0].imshow(masks[i], cmap='gray')
        ax[1, 0].set_title(u'节点')
        ax[1, 1].imshow(imgs[i] * masks[i], cmap='gray')
        ax[1, 1].set_title(u'节点切片')
        plt.show()
        print ('\n\n')
        # raw_input("hit enter to cont : ")


# 只显示结节
def make_mask(center, diam, z, width, height, spacing, origin):
    '''
        Center : 圆的中心 px -- list of coordinates x,y,z
        diam : 圆的直径 px -- diameter
        widthXheight : pixel dim of image
        spacing = mm/px conversion rate np array x,y,z
        origin = x,y,z mm np.array
        z = z position of slice in world coordinates mm
    '''
    mask = np.zeros([height, width])
    # 0's everywhere except nodule swapping x,y to match img
    # convert to nodule space from world coordinates

    # Defining the voxel range in which the nodule falls
    v_center = (center - origin) / spacing
    v_diam = int(diam / spacing[0] + 5)
    v_xmin = np.max([0, int(v_center[0] - v_diam) - 5])
    v_xmax = np.min([width - 1, int(v_center[0] + v_diam) + 5])
    v_ymin = np.max([0, int(v_center[1] - v_diam) - 5])
    v_ymax = np.min([height - 1, int(v_center[1] + v_diam) + 5])

    v_xrange = range(v_xmin, v_xmax + 1)
    v_yrange = range(v_ymin, v_ymax + 1)

    # Convert back to world coordinates for distance calculation
    x_data = [x * spacing[0] + origin[0] for x in range(width)]
    y_data = [x * spacing[1] + origin[1] for x in range(height)]

    # Fill in 1 within sphere around nodule
    for v_x in v_xrange:
        for v_y in v_yrange:
            p_x = spacing[0] * v_x + origin[0]
            p_y = spacing[1] * v_y + origin[1]
            if np.linalg.norm(center - np.array([p_x, p_y, z])) <= diam:
                mask[int((p_y - origin[1]) / spacing[1]), int((p_x - origin[0]) / spacing[0])] = 1.0
    return (mask)


def matrix2int16(matrix):
    ''' 
        matrix must be a numpy array NXN
        Returns uint16 version
    '''
    m_min = np.min(matrix)
    m_max = np.max(matrix)
    matrix = matrix - m_min
    return (np.array(np.rint((matrix - m_min) / float(m_max - m_min) * 65535.0), dtype=np.uint16))


#
# Helper function to get rows in data frame associated
# with each file
def get_filename(file_list, case):
    for f in file_list:
        if case in f:
            return (f)


#
# The locations of the nodes


def normalize(image, MIN_BOUND=-1000.0, MAX_BOUND=400.0):
    """数据标准化"""
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image
    # ---数据标准化


def set_window_width(image, MIN_BOUND=-1000.0, MAX_BOUND=400.0):
    """设置窗宽"""
    image[image > MAX_BOUND] = MAX_BOUND
    image[image < MIN_BOUND] = MIN_BOUND
    return image
    # ---设置窗宽
