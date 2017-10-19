import numpy as np
import pylab
import scipy.io as scio


GYRO_RATE = 25  # Hz


def get_distance(measure):
    return 1/measure


def update_angular_position(actual_position, angular_speed):
    return actual_position + angular_speed / GYRO_RATE


def main():
    data = scio.loadmat("Q1DonneesBon.mat")

    distance_sensor_measures = np.array(data['z'][0])
    gyro_measures = np.array(data['g'][0])

    angular_position = 0

    M = np.array([])
    for angular_speed,distance_measure in (gyro_measures, distance_sensor_measures):
        angular_position = update_angular_position(angular_position, angular_speed)
        distance = get_distance(distance_measure)
        M = np.vstack([M, [angular_position, distance]])

    pylab.plot(M, 'ro')


if __name__ == "__main__":
    main()
