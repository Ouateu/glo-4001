from scipy import ndimage
import matplotlib.pyplot as plt

import fast


DEFAULT_THRESHOLD = 10


def main():
    f = ndimage.imread("../res/bw-rectified-left-022146small.png")

    corners = {}
    max_v, max_u = f.shape
    print(f.shape)
    plt.imshow(f, cmap='gray')
    for v in range(max_v - 14):
        for u in range(max_u - 14):
            center = fast.Point(u, v)
            detector = fast.Fast(f, center, DEFAULT_THRESHOLD)
            is_corner, intensity = detector.detection_coin_fast()
            if is_corner:
                corners[center] = intensity
                plt.plot(v, u, 'ro')

    plt.show()


if __name__ == "__main__":
    main()
