import numpy as np
from skimage import morphology
from skimage import measure
from sklearn.cluster import KMeans
from skimage.transform import resize
from glob import glob
import shutil

# subset = "train_dataset/"
subset = "data_set/"
# working_path = "/home/ucla/Downloads/tianchi/" + subset
working_path = "/home/jenifferwu/IMAGE_MASKS_DATA/" + subset

file_list = glob(working_path + "images_*.npy")
out_images = []
for img_file in file_list:
    imgs_to_process = np.load(img_file).astype(np.float64)
    print("on image", img_file)
    for i in range(len(imgs_to_process)):
        img = imgs_to_process[i]
        out_images.append(img)

num_images = len(out_images)
rand_i = np.random.choice(range(num_images), size=num_images, replace=False)
test_i = int(0.2 * num_images)

for img_file in file_list:
    for i in range(test_i, num_images):
        img = imgs_to_process[i]
        train_dir = "train/"
        shutil.copy(img, working_path + train_dir)

    for i in range(test_i):
        img = imgs_to_process[i]
        test_dir = "test/"
        shutil.copy(img, working_path + test_dir)


