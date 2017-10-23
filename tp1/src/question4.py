from scipy import ndimage
import matplotlib.pyplot as plt

import fast


class Corner:

    def __init__(self, point, intensity):
        self.point = point
        self.intensity = intensity

    def __eq__(self, other):
        assert(isinstance(other, Corner))
        return self.intensity == other.intensity

    def __lt__(self, other):
        assert(isinstance(other, Corner))
        return self.intensity < other.intensity


DEFAULT_THRESHOLD = 100


def main():
    f = ndimage.imread("../res/bw-rectified-left-022146small.png")

    corners = []
    max_u, max_v = f.shape
    print(f.shape)
    for u in range(max_u - 14):
        print("Col: {}".format(u))
        for v in range(max_v - 14):
            center = fast.Point(u, v)
            detector = fast.Fast(f, center, DEFAULT_THRESHOLD)
            is_corner, intensity = detector.detection_coin_fast()
            if is_corner:
                corner = Corner(center, intensity)
                corners.append(corner)

    print("Nombre de coins: {}".format(len(corners)))
    corners.sort()
    xs = [corner.point.x for corner in corners]
    ys = [corner.point.y for corner in corners]
    plt.imshow(f, cmap='gray')
    plt.plot(ys, xs, 'ro')
    plt.show()


if __name__ == "__main__":
    main()
