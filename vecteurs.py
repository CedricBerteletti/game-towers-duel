# coding: utf-8
"""
Module de gestion des vecteurs
"""

from math import cos, sin, sqrt, atan2

    
def convertir_polaire(r, theta):
    """Fonction pour convertir des coordonnées polaires vers les coordonnées cartésiennes"""
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y


class Vecteur(object):
    """Classe pour un vecteur 2D simple"""

    def __init__(self, x=0, y=0):
        """Constructeur : initialisation du vecteur avec les coordonnées cartésiennes (x, y)"""
        self._x = x
        self._y = y

    def __str__(self):
        s = "<(" + \
            str(self.x) + ", " + str(self.y) + "), (" + \
            str(self.r) + ", " + str(self.theta) + " rad)>"
        return s

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def r(self):
        return sqrt(self._x * self._x + self._y * self._y)

    @r.setter
    def r(self, value):
        self._x, self._y = convertir_polaire(value, self.theta)

    @property
    def theta(self):
        return atan2(self._y, self._x)

    @theta.setter
    def theta(self, value):
        self._x, self._y = convertir_polaire(self.r, value)
