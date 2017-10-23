class Point:

    DEFAULT_CENTER = 3, 3

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_offset(self):
        off_x, off_y = self.DEFAULT_CENTER
        return Point(self.x - off_x, self.y - off_y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        assert(isinstance(other, Point))
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        return iter([self.x, self.y])

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


BEST_OFFSET = [Point(0, 3), Point(6, 3), Point(3, 6), Point(3, 0)]
OFFSETS = [Point(0, 3), Point(0, 4), Point(1, 5), Point(2, 6),
           Point(3, 6), Point(4, 6), Point(5, 5), Point(6, 4),
           Point(6, 3), Point(6, 2), Point(5, 1), Point(4, 0),
           Point(3, 0), Point(2, 0), Point(1, 1), Point(0, 2)]
MINIMAL_AMOUNT_OF_PIXELS = 12


class Fast:

    def __init__(self, image, center, threshold):
        self.image = image
        self.center = center
        self.threshold = threshold
        cx, cy = self.center
        self.center_value = self.image[cx][cy]

    def detection_coin_fast(self):
        valid_best_offset = []
        for offset in BEST_OFFSET:
            if self.is_candidate(offset):
                valid_best_offset.append(offset)

        if len(valid_best_offset) < 3:
            return False, 0

        contiguous_point = self.check_for_contiguous_point()
        if contiguous_point:
            return True, sum([abs(self.center_value - self.get_value(point)) for point in contiguous_point])
        else:
            return False, 0

    def is_candidate(self, offset):
        value = self.get_value(offset)
        return value < self.center_value - self.threshold or value > self.center_value + self.threshold

    def check_for_contiguous_point(self):
        contiguous_point = []
        for i in range(0, 32):
            offset = OFFSETS[i%16]
            if self.is_candidate(offset):
                contiguous_point.append(offset)
            elif len(contiguous_point) >= 12:
                return contiguous_point
            else:
                contiguous_point = []

            if 32 - i + len(contiguous_point) < 12:
                return False
            if len(contiguous_point) == 16:
                return contiguous_point
        return contiguous_point

    def get_value(self, point):
        point_coord = self.center + point.to_offset()
        x, y = point_coord
        return self.image[x, y]

    def display_image(self):
        display = "|"
        for i in range(0, 7):
            for j in range(0, 7):
                 display += " ( {} )".format(self.image[i, j])
            display += " |\n|"

        print(display)


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