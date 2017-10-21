from scipy import ndimage
import matplotlib.pyplot as plt


class Fast:

    def __init__(self, image):
        self.image = image


def main():
    f = ndimage.imread("../res/bw-rectified-left-022146small.png")

    print(f)
    plt.imshow(f, cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()
