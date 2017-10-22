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


def distance(p1, p2):
    return np.sqrt((p2[0,0] - p1[0,0])**2 + (p2[1,0] - p1[1,0])**2)

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


def circle_from_pts_and_angle(pts, angle):
    """
    Construit un cercle à partir de deux points de ce cercle et de l'angle
    entre ces deux points vu par un objet qui est aussi sur le cercle. pts doit
    être un tuple de points. Le point le plus à gauche doit toujours être donné
    en premier.
    """
    (p1, p2) = pts

    q = distance(p1,p2)
    m = (p1 - p2) / 2. + p2                      # Point milieu entre les deux points connus
    v = np.array([[0, -1], [1, 0]]).dot(m - p2)  # Vecteur perpendiculaire à la droite reliant p1 et p2

    l = (q / 2) / np.tan(np.radians(angle))      # Distance entre le points milieu et le centre du cercle

    v = (v / lin.norm(v)) * l                    # Ajustement de la longueur du vecteur

    c = m + v                                        # Centre du cercle
    r = np.fabs((q / 2.) / np.sin(np.radians(angle)))# Rayon du cercle

    return (c.transpose()[0], r)


# Implementation de la loi des cos
def get_c_from_cos_law(a, b, theta):
    c_square = (a**2) + (b**2) - 2*a*b*(np.cos(theta))
    c = np.sqrt(c_square)
    return c


def get_circle_intersections(c0x, c0y, r0, c1x, c1y, r1):
    d = m.sqrt(((c0x - c1x)**2) + ((c0y - c1y)**2))
    a = ((r0**2) - (r1**2) + (d**2))/(2*d)
    h = m.sqrt((r0**2)-(a**2))

    p_milieu_x = c0x + ((a(c1x - c0x))/d)
    p_milieu_y = c0y + ((a(c1y - c0y))/d)

    p_intersection1_x = p_milieu_x + (h*(c1x - c0x))/d
    p_intersection1_y = p_milieu_y - (h*(c1y - c0y))/d

    p_intersection2_x = p_milieu_x - (h*(c1x - c0x))/d
    p_intersection2_y = p_milieu_y + (h*(c1y - c0y))/d

    return p_intersection1_x, p_intersection1_y, p_intersection2_x, p_intersection2_y



