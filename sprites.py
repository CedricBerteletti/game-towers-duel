# coding: utf-8
"""
Module de gestion des sprites
"""

import pygame
import os
import math
from vecteurs import *
import time
#from projectiles import *

def charger_png(name):
    """Charge une image"""
    fullname = os.path.join('data', 'sprites', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        rect = image.get_rect()
    except pygame.error as message:
        print("Impossible de charger l'image : ", fullname)
        raise SystemExit
    return image, rect

def charger_son(name):
    """Charger un son"""
    fullname = os.path.join('data', 'sons', name)
    son = pygame.mixer.Sound(fullname)
    return son


class Sprite(pygame.sprite.Sprite):
    """Classe de base pour la gestion des sprites dans le jeu"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 0, 0)

    def charger_png(self, name):
        """Charge une image"""
        self.image, self.rect = charger_png(name)

    def update(self):
        pygame.sprite.Sprite.update(self)


class SpritePesant(Sprite):
    """
    Classe gérant les sprites soumis à la gravité
    La classe contient notamment les propriétés :
    _ image (héritée de Sprite)
    _ rect (héritée de Sprite), qui représente la position courante du sprite
    _ velocity, qui représente la vitesse courante du sprite.
    A l'appel de la méthode reset_movement(), la position et la vitesse instantanées du sprite deviennent \
        les nouvelles position et vitesse initiales, à partir desquelles les position et vitesse \
        instantanées sont calculées par les équations du mouvement. L'utilisation d'une position et \
        d'une vitesse initiales, conservées pendant tout le mouvement, permet d'éviter les arrondis \
        successifs entre chaque image du jeu.
    """

    def __init__(self):
        Sprite.__init__(self)
        self.gravite = 9.81      # accélération terrestre verticale en m/s²
        self.echelle = 1           # 1 pixel représente 1 m
        self.vitesse = Vecteur(0.0, 0.0)    # vitesse instantanée du sprite
        self.afficher_vecteur_vitesse = False  # Débogage : vecteur vitesse
        

    def init_mouvement(self):
        self._derniere_position_init = (self.rect.x, self.rect.y)
        self._derniere_vitesse_init = (self.vitesse.x, self.vitesse.y)
        self._dernier_temps_init = time.time()
        self._derniere_image_init = self.image

    def update(self):
        temps_ecoule = time.time() - self._dernier_temps_init
        # print(time_elapsed)
        x, y = self._derniere_position_init
        vx, vy = self._derniere_vitesse_init
        self.rect.x = x + self.echelle * (vx * temps_ecoule)
        self.rect.y = y + self.echelle * \
            (vy * temps_ecoule + 0.5 * self.gravite * temps_ecoule * temps_ecoule)
        self.vitesse.y = vy + self.gravite * temps_ecoule

        if self.afficher_vecteur_vitesse:
            self.image = self._derniere_image_init.copy()
            cx, cy = self.rect.width/2, self.rect.height/2
            pygame.draw.line(self.image, (255,0,0), (cx, cy),
                (cx + self.vitesse.x /self.echelle, cy + self.vitesse.y/self.echelle))
       

LONGUEUR_RETOUR_FLECHE = 10

class Fleche(Sprite):
    """
    Classe affichant une flèche
    """

    def __init__(self):
        Sprite.__init__(self)
        self.vecteur = Vecteur(10, 10)
        self.couleur = (1, 1, 1)

    def update(self):
        cx = self.rect.centerx        
        cy = self.rect.centery
        x, y = self.vecteur.x, self.vecteur.y
        ax, ay = abs(x)+LONGUEUR_RETOUR_FLECHE, abs(y)+LONGUEUR_RETOUR_FLECHE
        self.image = pygame.Surface([2 * int(ax), 2 * int(ay)])
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.image.set_colorkey((0, 0, 0))
        #self.image.fill((250, 250, 250))
        pygame.draw.line(self.image, self.couleur, (ax, ay), (ax + x, ay + y))

        cote = Vecteur(x / self.vecteur.r, y / self.vecteur.r)
        cote.r = cote.r * LONGUEUR_RETOUR_FLECHE
        cote.theta = cote.theta + math.pi/6
        pygame.draw.line(self.image, self.couleur, (ax+x - cote.x, ay+y - cote.y), (ax+x, ay+y))

        cote = Vecteur(x / self.vecteur.r, y / self.vecteur.r)
        cote.r = cote.r * LONGUEUR_RETOUR_FLECHE
        cote.theta = cote.theta - math.pi/6
        pygame.draw.line(self.image, self.couleur, (ax+x - cote.x, ay+y - cote.y), (ax+x, ay+y))

