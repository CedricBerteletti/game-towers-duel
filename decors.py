# coding: utf-8
"""
Module de gestion des décors
"""

import pygame
from sprites import charger_png, Sprite
from projectiles import Coco

class Decor(object): 
    """Classe générique pour gérer un décor"""

    def __init__(self, ecran):
        self.ecran = ecran
        self.sprites = pygame.sprite.Group()
        self.image = None
        self.projectiles = pygame.sprite.Group()



class Desert(Decor): 
    """Classe pour le décor désert"""

    def __init__(self, ecran):
        Decor.__init__(self, ecran)
        i, __ = charger_png("desert.png")
        self.image = pygame.transform.scale(i, ecran.get_size())
        
        s = Sprite()
        s.image = pygame.Surface([80, 65])        
        s.image.set_colorkey((0, 0, 0))
        #s.image.fill((250, 250, 250))
        s.rect = s.image.get_rect()
        s.rect.top = 245
        s.rect.left = 395
        self.sprites.add(s)
        
        s = Sprite()
        s.image = pygame.Surface([20, 65])        
        s.image.set_colorkey((0, 0, 0))
        #s.image.fill((250, 250, 250))
        s.rect = s.image.get_rect()
        s.rect.top = 300
        s.rect.left = 420
        self.sprites.add(s)

    
    def gerer_collisions(self, projectiles):
        # Si un projectile percute l'un des sprites du décor, le projectile disparaît et
        # le décor peut réagir
        supprimer_decor = False
        supprimer_projectile = True
        decors_impacts = pygame.sprite.groupcollide(self.sprites, projectiles, supprimer_decor, supprimer_projectile)
        for decors_impact in decors_impacts:
            b = Coco()
            b.rect.centerx = 450
            b.rect.centery = 270
            b.echelle = 1
            b.vitesse.x = 0
            b.vitesse.y = 0
            b.gravite = 50
            #b.afficher_vecteur_vitesse = True
            b.init_mouvement()
            self.projectiles.add(b)
    
    
    
