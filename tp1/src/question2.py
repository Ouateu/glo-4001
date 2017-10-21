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
