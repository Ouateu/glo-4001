import matlab
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
import math as m

FOCAL_DISTANCE = 1200 #Pixels

def make_image_uv_pose(Lx, Ly, Lz):
    u = (f/Lz)*Lx
    v = (f/Lz)*Ly
    return u, v

# Code du laboratoire qui retrouve les angles alpha et beta avec des positions dans l'image
def alpha_beta_from_three_coordinates(f, c1, c2, c3):
    """
    Retourne l'angle entre l'objet 1 et 2 (alpha), puis l'angle entre l'objet 2 et 3 (beta).
    Les arguments c1, c2, c3 sont la position en x de chaque objet dans l'image. f est la
    longueur focale.
    """
    position_of_optical_axis = 320

    positions = np.array([c1,c2,c3])
    thetas = np.degrees(np.arctan((positions - position_of_optical_axis) / f))

    return (thetas[1] - thetas[0], thetas[2] - thetas[1])

# Implementation de la loi des cos
def get_c_from_cos_law(a, b, theta):
    c_square = (a**2) + (b**2) - 2*a*b*(np.cos(theta))
    c = np.sqrt(c_square)
    return c

def get_circle_intersection(c0x, c0y, r0, c1x, c1y, r1):
    d = m.sqrt(((c0x - c1x)**2) + ((c0y - c1y)**2))
    a = ((r0**2) - (r1**2) + (d**2))/(2*d)
    h = m.sqrt((r0**2)-(a**2))
    
    

