import math as m


def gauss(x, sigma):
    return m.exp(-(x**2) / (2 * (sigma ** 2))) / m.sqrt(2 * m.pi * (sigma ** 2))
