import numpy as np
#import matplotlib.pyplot as plt
#import scipy.io as scio
import math as m

FOCAL_DISTANCE = 1200 #Pixels

def make_image_uv_pose(f, Lx, Ly, Lz):
    u = (f/Lz)*Lx
    v = (f/Lz)*Ly
    return int(u), int(v)


def distance(p1, p2):
    return np.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)

def norm(p):
    return np.sqrt((p['x'])**2 + (p['y'])**2)


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


def circle_from_pts_and_angle(p1, p2, angle):
    """
    Construit un cercle à partir de deux points de ce cercle et de l'angle
    entre ces deux points vu par un objet qui est aussi sur le cercle. pts doit
    être un tuple de points. Le point le plus à gauche doit toujours être donné
    en premier.
    """

    q = distance(p1, p2)
    m = dict()
    m['x'] = (p1['x'] - p2['x']) / 2. + p2['x']
    m['y'] = (p1['y'] - p2['y']) / 2. + p2['y']

    m_array = np.array([ [ m['x'] - p2['x'] ], [ m['y'] - p2['y'] ] ])
    v_array = np.array([[0, -1], [1, 0]]).dot(m_array)  # Vecteur perpendiculaire à la droite reliant p1 et p2

    v = dict()
    v['x'] = v_array[0, 0]
    v['y'] = v_array[1, 0]

    l = (q / 2) / np.tan(np.radians(angle))      # Distance entre le points milieu et le centre du cercle

    v['x'] = (v['x'] / norm(v)) * l     # Ajustement de la longueur du vecteur
    v['y'] = (v['y'] / norm(v)) * l     # Ajustement de la longueur du vecteur

    c = dict()
    c['x'] = m['x'] + v['x']      # Centre du cercle
    c['y'] = m['y'] + v['y']      # Centre du cercle
    r = np.fabs((q / 2.) / np.sin(np.radians(angle)))# Rayon du cercle

    return ([c['x'], c['y']], r)


def get_circle_intersections(c0, r0, c1, r1):
    c0x = float(c0[0])
    c0y = float(c0[1])
    c1x = float(c1[0])
    c1y = float(c1[1])

    d = m.sqrt(((c0x - c1x)**2) + ((c0y - c1y)**2))
    a = ((r0**2) - (r1**2) + (d**2))/(2*d)
    h = m.sqrt((r0**2)-(a**2))

    p_milieu_x = c0x + ((a*(c1x - c0x))/d)
    p_milieu_y = c0y + ((a*(c1y - c0y))/d)

    p_intersection1_x = p_milieu_x + (h*(c1x - c0x))/d
    p_intersection1_y = p_milieu_y - (h*(c1y - c0y))/d

    p_intersection2_x = p_milieu_x - (h*(c1x - c0x))/d
    p_intersection2_y = p_milieu_y + (h*(c1y - c0y))/d

    return p_intersection1_x, p_intersection1_y, p_intersection2_x, p_intersection2_y

def get_gauss(ecart_type):
    return 0

def loop_question23(metres_recule, ecart_type):
    L1 = {'x': -0.25, 'y': 0, 'z': 1.25}
    L2 = {'x': 0, 'y': 0, 'z': 1}
    L3 = {'x': 0.25, 'y': 0, 'z': 1.25}

    L = [L1, L2, L3]
    f = FOCAL_DISTANCE

    u_points = list()

    for i in range(0, len(L)):
        u, v = make_image_uv_pose(f, L[i]['x'], L[i]['y'], L[i]['z'])
        u_points.append(u)

    alpha, beta = alpha_beta_from_three_coordinates(f, u_points[0], u_points[1], u_points[2])

    for l in L:
        l['y'] = l['z']
        l['z'] = 0

    c0, r0 = circle_from_pts_and_angle(L[0], L[1], alpha)
    c1, r1 = circle_from_pts_and_angle(L[1], L[2], beta)

    return get_circle_intersections(c0, r0, c1, r1)

def main():
    L1 = {'x': -0.25, 'y': 0, 'z': 1.25}
    L2 = {'x': 0, 'y': 0, 'z': 1}
    L3 = {'x': 0.25, 'y': 0, 'z': 1.25}

    L = [L1, L2, L3]
    f = FOCAL_DISTANCE

    u_points = list()

    print("======= Question 2.1 =======")
    for i in range(0, len(L)):
        print("L{}:".format(i + 1))
        u, v = make_image_uv_pose(f, L[i]['x'], L[i]['y'], L[i]['z'])
        u_points.append(u)
        print("u: {} pixels, v: {} pixels".format(u, v))

    print("======= Question 2.2 =======")
    alpha, beta = alpha_beta_from_three_coordinates(f, u_points[0], u_points[1], u_points[2])
    print("alpha: {}°, beta: {}°".format(round(alpha, 2), round(beta, 2)))

    print("calcul des cercles...")
    for l in L:
        l['y'] = l['z']
        l['z'] = 0

    c0, r0 = circle_from_pts_and_angle(L[0], L[1], alpha)
    c1, r1 = circle_from_pts_and_angle(L[1], L[2], beta)

    print("c0: {}, r0: {}".format(c0, r0))
    print("c1: {}, r1: {}".format(c1, r1))
    print("Intersections obtenues:")

    pi1_x, pi1_y, pi2_x, pi2_y = get_circle_intersections(c0, r0, c1, r1)
    print("P1: {}, {}".format(pi1_x, pi1_y))
    print("P2: {}, {}".format(pi1_x, pi1_y))

    ecart_type = 2
    print("======= Question 2.3 =======")
        for i in range(0, 7):
            for j in range(0, 1000):
                loop_question23(i, ecart_type) 


if __name__ == "__main__":
    main()
