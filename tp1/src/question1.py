import math
import matlab
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
import math as m


GYRO_RATE = 25  # Hz
TRANSLATION_X = 10
TRANSLATION_Y = 1.7
THETA = math.pi/4


def get_distance(measure):
    if measure > 0:
        return 1/measure
    else:
        return 0


def update_angular_position(actual_position, angular_speed):
    new_angular_position = actual_position + angular_speed / GYRO_RATE
    unwraped_position = np.unwrap([new_angular_position])[0]
    return unwraped_position


def main():
    data = scio.loadmat("Q1DonneesBon.mat")

    distance_sensor_measures = np.array(data['z'][0])
    gyro_measures = np.array(data['g'][0])

    angular_position = 0

    angular_position_by_time = []
    distance_by_time = []
    for angular_speed, distance_measure in zip(gyro_measures, distance_sensor_measures):
        angular_position = update_angular_position(angular_position, angular_speed)
        distance = get_distance(distance_measure)

        if distance > 0:
            angular_position_by_time.append(angular_position)
            distance_by_time.append(distance)

    xs = []
    ys = []
    for angular_position, distance in zip(angular_position_by_time, distance_by_time):
        xs.append(distance * m.cos(angular_position))
        ys.append(distance * m.sin(angular_position))

    # plt.plot(xs, ys, 'ro')
    # plt.title("Nuage de point avec le robot en (0, 0, 0).")
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.show()

    p = np.matrix([xs, ys])
    p_homogeneous = np.vstack([p, [1 for i in range(len(xs))]])

    p_t = np.matrix([[1, 0, TRANSLATION_X], [0, 1, TRANSLATION_Y], [0, 0, 1]])
    p_r = np.matrix([[math.cos(THETA), -math.sin(THETA), 0], [math.sin(THETA), math.cos(THETA), 0], [0, 0, 1]])
    p_transform = np.matmul(p_t, p_r)
    p_global= np.matmul(p_transform, p_homogeneous)
    real_map = scio.loadmat("Carte.mat")
    plt.plot(real_map['Carte'][0], real_map['Carte'][1])
    plt.plot(p_global[0], p_global[1], 'ro')
    plt.show()


if __name__ == "__main__":
    main()
