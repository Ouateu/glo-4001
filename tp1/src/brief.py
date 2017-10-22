import random


S = 15


def extract_brief(patch, brief_descriptor_config):
    seed = brief_descriptor_config['seed']
    random.seed(seed)
    number_of_pair = brief_descriptor_config['pairs']
    descriptor = []
    for i in range(number_of_pair):
        x1, y1 = _get_random_point()
        x2, y2 = _get_random_point()
        p1 = patch[x1][y1]
        p2 = patch[x2][y2]
        if p1 > p2:
            descriptor.append(1)
        else:
            descriptor.append(0)
    return descriptor


def compute_hamming_distance(first_descriptor, second_descriptor):
    distance = 0
    for d1, d2 in zip(first_descriptor, second_descriptor):
        if d1 != d2:
            distance += 1
    return distance


def _get_random_point():
    return random.randint(0, S-1), random.randint(0, S-1)
