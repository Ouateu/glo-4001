import matplotlib.pyplot as plt
from scipy import ndimage

import fast

DEFAULT_THRESHOLD = 10


def main():
    f = ndimage.imread("../res/bw-rectified-left-022146small.png")

    corners = []
    max_y, max_x = f.shape
    print(f.shape)
    for y in range(max_y - 16):
        print("Col: {}".format(y))
        for x in range(max_x - 16):
            print("(x, y): ({}, {})".format(x, y))
            center = fast.Point(x+8, y+8)
            detector = fast.Fast(f, center, DEFAULT_THRESHOLD)
            is_corner, intensity = detector.detection_coin_fast()
            if is_corner:
                corner = fast.Corner(center, intensity)
                corners.append(corner)

    print("Nombre de coins: {}".format(len(corners)))
    corners.sort()
    xs = [corner.point.x for corner in corners]
    ys = [corner.point.y for corner in corners]
    plt.imshow(f, cmap='gray')
    plt.plot(xs, ys, 'ro')
    plt.show()


if __name__ == "__main__":
    main()
