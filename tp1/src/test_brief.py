from hamcrest import *
import unittest

import numpy as np

import brief


DEFAULT_HEIGHT = 15
DEFAULT_WIDTH = 15
DEFAULT_SHAPE = (DEFAULT_HEIGHT, DEFAULT_WIDTH)
DEFAULT_SEED = 1
DEFAULT_NUMBER_OF_PAIRS = 128


class TestBrief(unittest.TestCase):

    def setUp(self):
        self.empty_patch = np.ndarray(shape=DEFAULT_SHAPE)
        for i in range(DEFAULT_HEIGHT):
            for j in range(DEFAULT_WIDTH):
                self.empty_patch[i][j] = 0

        self.config = {'pairs': DEFAULT_NUMBER_OF_PAIRS,
                       'seed': DEFAULT_SEED}

        self.alternate_patch = np.ndarray(shape=DEFAULT_SHAPE)
        for i in range(DEFAULT_HEIGHT):
            for j in range(DEFAULT_WIDTH):
                self.alternate_patch[i][j] = (i + j) % 2

    def test_givenDescriptorWith128Pairs_whenExtractBrief_thenReturn128Pairs(self):
        expected_pairs = DEFAULT_NUMBER_OF_PAIRS

        descriptor = brief.extract_brief(self.empty_patch, self.config)

        assert_that(len(descriptor), is_(expected_pairs))

    def test_givenEmptyPatch_whenExtractBrief_thenReturnZeroSumDescriptor(self):
        expected_sum = 0

        descriptor = brief.extract_brief(self.empty_patch, self.config)

        assert_that(sum(descriptor), is_(expected_sum))

    def test_givenAlternatePatch_whenExtractBrief_thenReturnCorrectSumDescriptor(self):
        expected_sum = 33

        descriptor = brief.extract_brief(self.alternate_patch, self.config)

        assert_that(sum(descriptor), is_(expected_sum))

    def test_givenSamePatchTwice_whenExtractBrief_thenReturnSameDescriptor(self):
        first_descriptor = brief.extract_brief(self.alternate_patch, self.config)
        second_descriptor = brief.extract_brief(self.alternate_patch, self.config)

        assert_that(first_descriptor, is_(second_descriptor))

    def test_givenTwoIdenticalDescriptor_whenComputeHammingDistance_thenDistanceIsZero(self):
        descriptor = [1, 1, 0, 1, 1]
        expected_distance = 0

        actual_distance = brief.compute_hamming_distance(descriptor, descriptor)

        assert_that(actual_distance, is_(expected_distance))

    def test_whenComputeHammingDistance_thenReturnCorrectDistance(self):
        first_descriptor = [1, 1, 1, 0, 0]
        second_descriptor = [1, 1, 1, 1, 1]
        expected_distance = 2

        actual_distance = brief.compute_hamming_distance(first_descriptor, second_descriptor)

        assert_that(actual_distance, is_(expected_distance))


if __name__ == "__main__":
    unittest.main()
