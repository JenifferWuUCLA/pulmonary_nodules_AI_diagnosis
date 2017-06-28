import numpy as np
from PIL import Image
from glob import glob
import cv2

# subset = "train_dataset/"
subset = "data_set/"
# working_path = "/home/ucla/Downloads/tianchi/" + subset
working_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset + "predictions/JPEG/"

# output_path = "/home/ucla/Downloads/Caffe_CNN_Data/"
output_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset + "predictions/JPEG/output/"

file_list = glob(working_path + "imgs_mask_test_*.jpg")
# file_list = glob(working_path + "masksTestPredicted.npy")

# print(working_path + "imgs_mask_test_*.jpg")
print(len(file_list))
max_size = len(file_list)

for i in range(len(file_list)):
    # imgs_to_process = np.load(img_file).astype(np.float64)
    # print(len(imgs_to_process))
    img_file = file_list[i]
    img_1 = file_list[i]
    img_2, img_3 = img_1, img_1
    if i + 1 < max_size:
        img_2 = file_list[i + 1]
    print(i + 2 <= max_size)
    if i + 2 < max_size:
        img_3 = file_list[i + 2]
    # print(img_1, img_2, img_3)
    i += 3
    print(i)
    # Load the 1st image
    base_img = Image.open(img_1)
    # print base_img.size, base_img.mode
    box = (166, 64, 320, 337)

    # Load the 2n image
    tmp_img = Image.open(img_2)
    region = tmp_img
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    base_img.paste(region, box)

    # Load the 3rd image
    tmp_img = Image.open(img_3)
    region = tmp_img
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    base_img.paste(region, box)

    filename = img_file.replace(working_path, "")
    new_name = filename.replace(".jpg", "") + "_%s.jpg" % (i)
    print("new_name: %s" % new_name)
    image_path = output_path + new_name
    print("image_path: %s" % image_path)
    base_img.show()
    base_img.save(image_path)
