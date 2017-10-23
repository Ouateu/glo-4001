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
    for u in range(max_u - 16):
        print("Col: {}".format(u + 8))
        for v in range(max_v - 16):
            center_point = fast.Point(u + 8, v + 8)
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
        print("Patch:\n {}".format(patch))
        descriptors[keypoint.point] = brief.extract_brief(patch, config)
    return descriptors


def get_patch(img, center):
    x, y = center
    print("Center: {}".format(center))
    return numpy.copy(img[y-7:y+8, x-7:x+8])


def find_appariement(left, right):
    appariement = {}
    for left_point in left:
        smallest_distance = 257
        associate_right_point = None
        for right_point in right:
            distance = brief.compute_hamming_distance(left[left_point], right[right_point])
            if distance < smallest_distance:
                smallest_distance = distance
                associate_right_point = right_point
        appariement[left_point] = associate_right_point
    return appariement


def main():
    img_left = ndimage.imread("../res/bw-rectified-left-022146small.png")
    img_right = ndimage.imread("../res/bw-rectified-right-022146small.png")

    descriptor_config = {'pairs': 256,
                         'seed': 1}
    left_descriptors = pipeline(img_left, descriptor_config)
    right_descriptors = pipeline(img_right, descriptor_config)

    appariement = find_appariement(left_descriptors, right_descriptors)
    plt.imshow(img_left, cmap='gray')

    x_lines = []
    y_lines = []
    for left_point, right_point in appariement.items():
        xl, yl = left_point
        xr, yr = right_point
        x_lines.append(numpy.linspace(xl, xr, 100))
        y_lines.append(numpy.linspace(yl, yr, 100))

    for x, y in zip(x_lines, y_lines):
        plt.plot(x, y, '-g')

    plt.show()


if __name__ == "__main__":
    main()