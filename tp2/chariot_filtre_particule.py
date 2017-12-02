
import numpy as np
import math as m
import matplotlib.pyplot as plt

# Systeme representant le chariot pour le TP3, Automne 2015
# (c) Philippe Giguere, 2015 Version 1.0

myFontSize = 14 # Taille de la police de caractere pour les graphes

# Parametre du systeme
d_init = 3.0    # Point de depart du robot
SAngle = 0.003  # �cart-type du bruit sur la mesure d'angle.
SV = 0.15       # �cart-type du bruit sur le voltage du moteur.
nStep = 400     # Nombres de mesures/pas
dT = 0.1        # Intervalle de temps entre les mesures/pas

# Important! Il faut initialiser la matrice X de facon a avoir
# une dimension (2,1) et non (1,2). Sinon, le filtre EKF ne marchera pas.
xVrai = [[d_init], [0.0]] # Etat reel, inconnu du filtre et du robot.

# Specifier les valeurs initiales des matrices.
# Ne pas oublier qu'ici, ce sont des covariances, pas des ecarts-types.
X = [[d_init], [0]]  # un exemple d'initialisation.

# Constantes pour le filtre a particules

nParticules = 40
Reff = 0.5

AxVrai1 = list()
AxVrai2 = list()
AX1 = list()
AX2 = list()
AU = list()
AZ = list()
ATime = list()

for iStep in range(1, nStep):
    # Simulation du systeme a chaque etape
    time = iStep*dT

    # Commande de voltage envoye vers le systeme.
    U = 8*m.sin(0.2*m.pi*time)

    # ============== Debut de la simulation du deplacement reel ===========   
    # Le deplacement veritable du chariot selon les equations.
    # Je vous donne les equations, vous n'avez rien a changer ici.

    xVrai[0][0] = xVrai[0][0] + (xVrai[1][0])*dT # Calcul du deplacement
    xVrai[1][0] = 2.*(1 / (1 + m.exp(-0.5 * (U + np.random.normal() * SV))) - 0.5)   # Calcul de la vitesse
    
    # Je simule pour vous la r�ponse de la cam�ra.
    # Le max(0.001,...) est pour �viter les valeurs n�gatives.
    z = max(0.001, 0.07 / xVrai[1][0] + SAngle * np.random.normal())

    # =============== Fin de la simulation de deplacement reel ============   

    # ================ Debut de votre filtre E K F ou particule ==================
    # ATTENTION ATTENTION ATTENTION ATTENTION
    # Vous n'avez pas le droit d'utiliser xVrai dans votre filtre
    # car c'est la position et la vitesse reele du systeme, et 
    # elles vous sont inconnues.

    ########## Votre code ici! #######

    # ========= Fin des equations du filtre EKF ou particule =============
    
    # Cueillette des donnees pour les graphiques/statistiques
    AxVrai1.append(xVrai[0][0])
    AxVrai2.append(xVrai[1][0])
    AX1.append(X[0][0])
    AX2.append(X[1][0])
    AU.append(U)
    AZ.append(z)
    ATime.append(time)
    
    # Pour voir votre filtre evoluer dans le temps
    plt.clf()

    plt.plot(ATime,AX1,'go', label='EKF')
    plt.plot(ATime,AxVrai1,'k-','LineWidth',2, label='Position Exacte')
    plt.plot(ATime, np.divide(0.07, AZ).tolist(), 'r*', label='Mesure h_z^{-1}') # Ici on peut inverser le capteur, pour trouver la position correspondant a z.

    plt.xlabel('Temps (s)')
    plt.ylabel('Estime de position (m)')
    plt.legend()

    plt.ylim(0, 20)

    plt.draw()
