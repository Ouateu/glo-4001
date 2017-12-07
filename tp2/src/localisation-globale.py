import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy.io as scio

from particule_resampling import particule_resampling
from gauss import gauss

def main():
    real_map = scio.loadmat("../res/Carte.mat")

    ### Inserer code de localisation ici
    lidar_direction = [0, m.pi/2, m.pi, (3*m.pi)/2]
    sig_Lidar = 0.01
    sig_vitesse = 0.01
    sig_omega = 0.05
    sig_compas = 0.01

    angle_compas = m.pi + np.random.normal()

    plt.plot(real_map['Carte'][0], real_map['Carte'][1])
    plt.show()


if __name__ == "__main__":
    main()

