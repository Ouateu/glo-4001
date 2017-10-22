import unittest
from hamcrest import *

import numpy as np

import fast
from fast import Fast


class TestPoint(unittest.TestCase):

    def setUp(self):
        self.first_point = fast.Point(5, 5)
        self.second_point = fast.Point(3, 3)

    def test_whenAdd_thenSecondPointIsAdded(self):
        expected = fast.Point(8, 8)

        actual = self.first_point + self.second_point

        assert_that(actual, is_(expected))

    def test_whenSub_thenSecondPointIsSubtracted(self):
        expected = fast.Point(2, 2)

        actual = self.first_point - self.second_point

        assert_that(actual, is_(expected))


class TestFast(unittest.TestCase):

    DEFAULT_IMAGE_LENGTH = 7
    DEFAULT_IMAGE_HEIGHT = 7
    DEFAULT_SHAPE = DEFAULT_IMAGE_LENGTH, DEFAULT_IMAGE_HEIGHT
    DEFAULT_CENTER = fast.Point(*fast.Point.DEFAULT_CENTER)
    DEFAULT_THRESHOLD = 0.5

    MINIMAL_NUMBER_OF_PIXELS = fast.MINIMAL_AMOUNT_OF_PIXELS

    def setUp(self):
        self.full_corner_image = self._create_image(fast.OFFSETS)
        self.no_corner_image = self._create_image(None)
        self.missing_one_image = self._create_image(fast.OFFSETS[0:self.MINIMAL_NUMBER_OF_PIXELS - 1])
        self.minimal_image = self._create_image(fast.OFFSETS[0:self.MINIMAL_NUMBER_OF_PIXELS])
        self.image5To16 = self._create_image(fast.OFFSETS[5-1:16])
        self.image4To15 = self._create_image(fast.OFFSETS[4-1:15])
        self.image8To3 = self._create_image(fast.OFFSETS[8-1:16])
        self.image8To3 = self._fill_image_range_with_one(self.image8To3, fast.OFFSETS[0:3+1])

        self.bright_image_with_dark_arc = self._create_image(fast.OFFSETS)
        self.bright_image_with_dark_arc[3][3] = 1
        for i, j in fast.OFFSETS[0:12]:
            self.bright_image_with_dark_arc[i][j] = 0

        self.semi_bright_corner_dark_image = self._create_image(None)
        for i, j in fast.OFFSETS[0:12]:
            self.semi_bright_corner_dark_image[i][j] = self.DEFAULT_THRESHOLD + 0.1

        self.semi_dark_corner_bright_image = self._create_image(None)
        for i in range(0, 7):
            for j in range(0, 7):
                self.semi_dark_corner_bright_image[i][j] = 1
        for i, j in fast.OFFSETS[0:12]:
            self.semi_dark_corner_bright_image[i][j] = self.DEFAULT_THRESHOLD - 0.1

    def test_givenNoCorner_whenDetectionCoinFast_thenIsNotCorner(self):
        cut = Fast(self.no_corner_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(False))

    def test_givenFullCornerMoreIntense_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.full_corner_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenImageWithOnePixelMissingForCorner_whenDetectionCoinFast_thenIsNotCorner(self):
        cut = Fast(self.missing_one_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(False))

    def test_givenImageWithMinimalPixelsForCorner_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.minimal_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenImageWith5To16_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.image5To16, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenImageWith4To15_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.image4To15, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenImageWith8To3_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.image8To3, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenImageWithDarkCorner_whenDetectionCoinFast_thenIsCorner(self):
        cut = Fast(self.bright_image_with_dark_arc, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        is_coin, _ = cut.detection_coin_fast()
        assert_that(is_coin, is_(True))

    def test_givenDarkImageWithBrightCorner_whenDetectionCoinFast_thenReturnCorrectIntensityValue(self):
        cut = Fast(self.full_corner_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        _, intensity_value = cut.detection_coin_fast()
        expected_intensity = 16
        assert_that(intensity_value, is_(expected_intensity))

    def test_givenDarkImageWithSemiBrightCorner_whenDetectionCointFast_thenReturnCorrectIntensityValue(self):
        cut = Fast(self.semi_bright_corner_dark_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        _, intensity_value = cut.detection_coin_fast()
        expected_intensity = (self.DEFAULT_THRESHOLD + 0.1) * 12
        self.assertAlmostEqual(expected_intensity, intensity_value, places=2)

    def test_givenBrightImageWithSemiDarkCorner_whenDetectionCoinFast_thenReturnCorrectIntensityValue(self):
        cut = Fast(self.semi_dark_corner_bright_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        _, intensity_value = cut.detection_coin_fast()
        expected_intensity = (1 - (self.DEFAULT_THRESHOLD - 0.1)) * 12
        self.assertAlmostEqual(expected_intensity, intensity_value, places=2)

    def test_givenFullCorner_whenDetectionCoinFast_thenReturnCorrectIntensityValue(self):
        cut = Fast(self.full_corner_image, self.DEFAULT_CENTER, self.DEFAULT_THRESHOLD)
        _, intensity_value = cut.detection_coin_fast()
        expected_intensity = 16
        self.assertAlmostEqual(expected_intensity, intensity_value)

    def _create_image(self, range_to_set):
        zeroed_image = self._fill_image_with_zero(np.ndarray(shape=self.DEFAULT_SHAPE))
        set_image = self._fill_image_range_with_one(zeroed_image, range_to_set)
        return set_image

    def _fill_image_with_zero(self, image):
        for i in range(0, self.DEFAULT_IMAGE_HEIGHT):
            for j in range(0, self.DEFAULT_IMAGE_LENGTH):
                image[i][j] = 0
        return image

    def _fill_image_range_with_one(self, image, range_to_set):
        if range_to_set is None:
            return image

        for i, j in range_to_set:
            image[i][j] = 1
        return image


if __name__ == "__main__":
    unittest.main()
