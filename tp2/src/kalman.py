import numpy as np
import math
import matplotlib.pyplot as plt

# Systeme representant le chariot pour le TP3, Automne 2015
# (c) Philippe Giguere, 2015 Version 1.0

myFontSize = 14  # Taille de la police de caractere pour les graphes

# Parametre du systeme
d_init = 3  # Point de depart du robot
S_angle = 0.003  # ecart-type du bruit sur la mesure d'angle.
S_volt = 0.15  # ecart-type du bruit sur le voltage du moteur.
S_speed = (2 * (1 / (1 + math.exp(-S_volt/2)) - 0.5))**2

number_steps = 400  # Nombres de mesures/pas
# number_steps = 50  # Nombres de mesures/pas
delta_t = 0.1  # Intervalle de temps entre les mesures/pas

# Important! Il faut initialiser la matrice X de facon a avoir
# une dimension (2,1) et non (1,2). Sinon, le filtre EKF ne marchera pas.
X_vrai = [[d_init], [0.0]]  # Etat reel, inconnu du filtre et du robot.

# Specifier les valeurs initiales des matrices.
# Ne pas oublier qu'ici, ce sont des covariances, pas des ecarts-types.
X = np.matrix(np.array([[d_init+1], [0]]))
P = np.matrix(np.array([[100, 0], [0, 1]]))

Ax_vrai1 = []
Ax_vrai2 = []
AX1 = []
AX2 = []
AU = []
AZ = []
ATime = []

for step in range(1, number_steps):
    # Simulation du systeme a chaque etape
    time = step * delta_t

    # Commande de voltage envoye vers le systeme.
    U = 8 * math.sin(0.2 * math.pi * time)

    # ============== Debut de la simulation du deplacement reel ===========   
    # Le deplacement veritable du chariot selon les equations.
    # Je vous donne les equations, vous n'avez rien a changer ici.

    X_vrai[0][0] = X_vrai[0][0] + (X_vrai[1][0]) * delta_t  # Calcul du deplacement
    X_vrai[1][0] = 2. * (1 / (1 + math.exp(-0.5 * (U + np.random.normal() * S_volt))) - 0.5)  # Calcul de la vitesse

    # Je simule pour vous la reponse de la camera.
    # Le max(0.001,...) est pour eviter les valeurs n�gatives.
    z = max(0.001, 0.07 / X_vrai[0][0] + S_angle * np.random.normal())
    # =============== Fin de la simulation de deplacement reel ============   

    # ================ Debut de votre filtre E K F ou particule ==================
    # Vous n'avez pas le droit d'utiliser xVrai dans votre filtre
    # car c'est la position et la vitesse reelle du systeme, et
    # elles vous sont inconnues.

    # Propagation
    X[0, 0] = X[0] + X[1] * delta_t
    X[1, 0] = 2 * (1 / (1 + math.exp(-U / 2)) - 0.5)

    # Jacobiennes
    F = np.matrix(np.array([[1, delta_t], [0, 0]]))
    G = np.matrix(np.array([[delta_t * (math.exp(U / 2) / (1 + math.exp(U / 2)) ** 2)],
                            [math.exp(U / 2) / (1 + math.exp(U / 2)) ** 2]]))
    H = np.matrix('{} 0'.format(-0.07 / X[0]**2))

    P = F * P * F.T + G * G.T * S_volt**2

    # Mise a jour
    K = (P * H.T) / (H * P * H.T + S_angle**2)
    z_predict = 0.07/X[0, 0]
    r = z - z_predict
    X = X + K * r
    P = (np.eye(2) - K*H) * P

    # ========= Fin des equations du filtre EKF ou particule =============

    # Cueillette des donnees pour les graphiques/statistiques
    Ax_vrai1.append(X_vrai[0][0])
    Ax_vrai2.append(X_vrai[1][0])
    AX1.append(X[0, 0])
    AX2.append(X[1, 0])
    AU.append(U)
    AZ.append(z)
    ATime.append(time)

    # Pour voir votre filtre evoluer dans le temps
    plt.clf()

    plt.plot(ATime, AX1, 'go', label='EKF')
    plt.plot(ATime, Ax_vrai1, 'k-', label='Position Exacte')
    plt.plot(ATime, np.divide(0.07, AZ).tolist(), 'r*', label='Mesure h_z^{-1}')

    plt.xlabel('Temps (s)')
    plt.ylabel('Estime de position (m)')
    plt.legend()

    plt.ylim(0, 20)

    plt.draw()

plt.show()
