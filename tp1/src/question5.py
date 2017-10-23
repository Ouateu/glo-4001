import math
import matplotlib.pyplot as plt
import numpy
from scipy import ndimage

import brief
import fast


DEFAULT_THRESHOLD = 100


def pipeline(img, descriptor_config):
    keypoints = extract_keypoint(img)
    strongest_keypoints = select_strongest(keypoints)
    descriptors = extract_descriptors(img, strongest_keypoints, descriptor_config)
    return descriptors


def extract_keypoint(img):
    max_u, max_v = img.shape
    corners = []
    for u in range(max_u - 14):
        print("Col: {}".format(u + 7))
        for v in range(max_v - 14):
            center_point = fast.Point(u + 7, v + 7)
            detector = fast.Fast(img, center_point, DEFAULT_THRESHOLD)
            is_corner, intensity = detector.detection_coin_fast()

            if is_corner:
                corner = fast.Corner(center_point, intensity)
                corners.append(corner)
    return corners


def select_strongest(points):
    number_of_points = len(points)
    points.sort()
    idx10 = math.floor(number_of_points * 0.1)
    print("Number of point selected: {}".format(idx10))
    return points[-idx10:]


def extract_descriptors(img, points, config):
    descriptors = {}
    for keypoint in points:
        patch = get_patch(img, keypoint.point)
        descriptors[keypoint.point] = brief.extract_brief(patch, config)
    return descriptors


def get_patch(img, center):
    x, y = center
    return numpy.copy(img[y-7:y+8,x-7:x+8])


def main():
    img_left = ndimage.imread("../res/bw-rectified-left-022146small.png")
    img_right = ndimage.imread("../res/bw-rectified-right-022146small.png")

    descriptor_config = {'pairs': 256,
                         'seed': 1}
    pipeline(img_left, descriptor_config)


if __name__ == "__main__":
    main()