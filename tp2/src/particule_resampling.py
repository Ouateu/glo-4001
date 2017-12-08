from collections import namedtuple

import numpy as np
import math as m


Resample = namedtuple('Resample', ['X', 'w'])

def particule_resampling(X, w, ratio):
    """
        ParticuleResampling   Pour effectuer le reechantillonnage des particules,
                              si necessaire
        [XResampled WResampled] = ParticuleResampling(X,w,Ratio)
          Entree
               X : matrice de DxN, de type np.array, ou N est le nombre de particules et D le
                   nombre de variable d'etat
               w : matrice de 1xN, ou N est le nombre de particules
           Ratio : Ratio effectif en-deca duquel on reechantillonne.

         Sortie : X et w reechantillonnes
         Ver 1.1
    """

    # Normaliser les poids w;
    nParticules = len(w)
    Wnorm = sum(w)
    w = np.divide(w, Wnorm).tolist()
    copy = [0] * nParticules
    
    # Resampling, pour combattre l'appauvrissement
    Neff = 1/sum([i**2 for i in w])
    
    if m.isnan(Neff):
        Neff = 0
        w = np.divide(([1] * nParticules), nParticules).tolist()


   
    # Verification si appauvrissement des particules
    if Neff < (ratio * nParticules):
        # Effectuer un resampling.        
        print('Resampling')

        Q = np.cumsum(w).tolist()
        sorted_array = np.sort(np.random.rand(nParticules+1), axis=None)
        T = sorted_array.tolist()

        T[nParticules] = 1

        index = 0
        jindex = 0

        while index < nParticules:
            if T[index] < Q[jindex]:
                copy[index] = jindex
                index = index + 1
            else:
                jindex = jindex + 1


        # Copie des particules, selon leur poids
        w = np.divide(([1] * nParticules), nParticules).tolist()
        Xt = np.transpose(X)
        newXt = Xt[copy]
        X = np.transpose(newXt)

    return X, w
