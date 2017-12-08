import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy.io as scio
import shapely.geometry as geo

from particule_resampling import particule_resampling
from gauss import gauss

def main():
    real_map = scio.loadmat("../res/Carte.mat")
    coord_carte = list(zip(real_map['Carte'][0], real_map['Carte'][1]))
    carte = geo.Polygon(coord_carte)

    AZx = list()
    AZy = list()
    ATime = list()

    ### Inserer code de localisation ici
    lidar_direction = [0, m.pi/2, m.pi, (3*m.pi)/2]
    lidar_distance_max = 20
    sig_Lidar = 0.01
    sig_vitesse = 0.01
    sig_omega = 0.05
    sig_compas = 0.01
    sig_angle = 0.01 # bruit à ajouter sur le compas magnétique

    n_step = 100
    dt = 0.1
    n_particules = 100 #nombres de particules
    Reff = 0.1 # Ratio effectif
    vitesse = 0

    Xvrai = np.transpose([[2, 1]])

    x = np.random.rand(n_particules, 1)*18
    y = np.random.rand(n_particules, 1)*8
    X = np.transpose(np.column_stack([x, y]))
    w = [1]*n_particules

    for i_step in range(0, n_step):
        time = i_step*dt
        angle_compas = np.random.normal()

        ### Simulation des vrais mesures ###
        Xvrai[0][0] = Xvrai[0][0] + dt*(vitesse + np.random.normal())*(round(m.cos(angle_compas), 100))
        Xvrai[1][0] = Xvrai[1][0] + dt*(vitesse + np.random.normal())*(round(m.sin(angle_compas), 100))


        # Estimation de la mesure du Lidar
        lidar_estimate = []
        for direction in lidar_direction:
            point_start_line = [Xvrai[0][0], Xvrai[1][0]]
            point_end_line = [point_start_line[0] + lidar_distance_max*(round(m.cos(direction), 100)),
                              point_start_line[1] + lidar_distance_max*(round(m.sin(direction), 100))]

            line = geo.LineString([point_start_line, point_end_line])
            intersection = np.array(carte.intersection(line))
            # Bruit sur le Lidar
            intersection[0] = intersection[0] + np.random.normal()
            intersection[1] = intersection[1] + np.random.normal()

            lidar_estimate.append(intersection)

        ### Fin simulation du monde

        # Filtre a particules
        line_x = geo.LineString([lidar_estimate[0], lidar_estimate[2]])
        line_y = geo.LineString([lidar_estimate[1], lidar_estimate[3]])
        intersection_position = np.array(line_x.intersection(line_y))


        for i_particule in range(0, n_particules):
            X[0][i_particule] = intersection_position[0]
            X[1][i_particule] = intersection_position[1]

            w[i_particule] = gauss(x=angle_compas, sigma=sig_angle) * w[i_particule]

        #X, w = particule_resampling(X=X, w=w, ratio=Reff)

        # ========= Fin des equations du filtre EKF ou particule =============

        # Cueillette des donnees pour les graphiques/statistiques
        AZx.append(intersection_position[0])
        AZy.append(intersection_position[1])
        ATime.append(time)


    myFontSize = 14 # Taille de la police de caractere pour les graphes
    plt.clf()

    plt.plot(real_map['Carte'][0], real_map['Carte'][1])
    plt.plot(np.transpose(X[0]), np.transpose(X[1]), 'b*', label = 'Particules au depart')
    #plt.plot(ATime, AX1, 'go', label='filtre a particules')
    plt.plot(AZx, AZy, 'r*', label='Mesure h_z^{-1}') # Ici on peut inverser le capteur, pour trouver la position correspondant a z.

    plt.xlabel('Temps (s)')
    plt.ylabel('Estime de position (m)')
    plt.legend()

    plt.draw()
    plt.show()


if __name__ == "__main__":
    main()

