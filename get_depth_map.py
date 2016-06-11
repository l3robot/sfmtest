import os
import sys
import time

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.style.use('ggplot')
import json

from scipy import interpolate

from plyfile import PlyData, PlyElement

# SPECS FOR NEXUS 5
FOCAL = 4
CAM_WIDTH = 4.54


def get_focal_pixel(focal_mm, cam_width_mm, image_width):
    return (focal_mm * image_width) / cam_width_mm


def get_ply(directory):

    images = os.path.join(directory, 'images')
    sparse = os.path.join(
        directory, 'results/reconstruction_global/robust_colorized.ply')
    sfm_data = os.path.join(
        directory, 'results/reconstruction_global/sfm_data.json')
    dense = os.path.join(
        directory, 'results/reconstruction_global/PMVS/models/pmvs_options.txt.ply')

    return images, sparse, sfm_data, dense


def get_cam_one_img(images, file):
    return mpimg.imread(os.path.join(images, file))


def get_cam_one_pos(sparse,
                    color_channel_names=('red', 'green', 'blue')):
    """
    Get camera positions.
    Camera positions are supposed to have RGB = (0, 255, 0) points.
    :returns: [[x, y, z], ...] camera positions.
    """
    plydata = PlyData.read(sparse)
    camId = (
        (plydata.elements[0][color_channel_names[0]] == 0) &
        (plydata.elements[0][color_channel_names[1]] == 255) &
        (plydata.elements[0][color_channel_names[2]] == 0)
    )
    camPos = np.vstack((plydata.elements[0]['x'],
                        plydata.elements[0]['y'],
                        plydata.elements[0]['z'])).T
    return camPos[camId, :][0]


def depth_map(dense, new_image, R, C, focal):
    plydata = PlyData.read(dense)

    pointPos = np.vstack((plydata.elements[0]['x'],
                        plydata.elements[0]['y'],
                        plydata.elements[0]['z'])).T    

    tx, ty = new_image.shape
    mx, my = new_image.shape
    mx = mx // 2
    my = my // 2

    for p in pointPos:
        p_c = R.dot(p)-R.dot(C)
        x, y = focal/p_c[2]*p_c[:2]
        if int(y) < mx and int(x) < my:
            new_image[int(y)+mx, int(x)+my] = C[2]-p_c[2]

    coords = new_image.nonzero()
    values = new_image[coords]

    coords = np.array([coords[0], coords[1]]).T

    xx = np.arange(0,tx)
    yy = np.arange(0,ty)

    xx, yy = np.meshgrid(xx, yy)

    f = interpolate.NearestNDInterpolator(coords, values)
    return f(xx, yy)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(' [ ! ] You have to give a directory')
        exit()

    directory = sys.argv[1]

    images, sparse, sfm_data, dense = get_ply(directory)
    pos = get_cam_one_pos(sparse)

    with open(sfm_data, 'r') as f:
        sfm_data = json.load(f)

    file = sfm_data['views'][0]['value']['ptr_wrapper']['data']['filename']
    focal = sfm_data['intrinsics'][0]['value'][
        'ptr_wrapper']['data']['focal_length']
    R = np.array(sfm_data['extrinsics'][0]['value']['rotation'])
    C = np.array(sfm_data['extrinsics'][0]['value']['center'])

    images = get_cam_one_img(images, file)

    # focal = get_focal_pixel(FOCAL, CAM_WIDTH, images.shape[1])

    new_image = np.zeros(images.shape[:2])

    new_image = depth_map(dense, new_image, R, C, focal)

    # print(new_image)

    fig = plt.figure()
    a=fig.add_subplot(1,2,1)

    plt.imshow(images)
    a=fig.add_subplot(1,2,2)
    plt.imshow(new_image.T, vmin=np.min(new_image), vmax=np.max(new_image), cmap="hot")
    plt.show()
